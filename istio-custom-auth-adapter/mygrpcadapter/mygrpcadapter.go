// nolint:lll
// Generates the mygrpcadapter adapter's resource yaml. It contains the adapter's configuration, name, supported template
// names (metric in this case), and whether it is session or no-session based.
//go:generate $GOPATH/src/istio.io/istio/bin/mixer_codegen.sh -a mixer/adapter/mygrpcadapter/config/config.proto -x "-s=false -n mygrpcadapter -t authorization"

package mygrpcadapter

import (
	"context"
	"fmt"
	"net"
	"strings"
	"time"

	"google.golang.org/grpc"

	"github.com/dgrijalva/jwt-go"

	"istio.io/api/mixer/adapter/model/v1beta1"
	policy "istio.io/api/policy/v1beta1"
	"istio.io/istio/mixer/adapter/mygrpcadapter/config"
	"istio.io/istio/mixer/pkg/status"
	"istio.io/istio/mixer/template/authorization"
	"istio.io/istio/pkg/log"
)

type (
	// Server is basic server interface
	Server interface {
		Addr() string
		Close() error
		Run(shutdown chan error)
	}

	// MyGrpcAdapter supports metric template.
	MyGrpcAdapter struct {
		listener net.Listener
		server   *grpc.Server
	}
)

var _ authorization.HandleAuthorizationServiceServer = &MyGrpcAdapter{}

// HandleMetric records metric entries
func (s *MyGrpcAdapter) HandleAuthorization(ctx context.Context, r *authorization.HandleAuthorizationRequest) (*v1beta1.CheckResult, error) {

	cfg := &config.Params{}

	if r.AdapterConfig != nil {
		if err := cfg.Unmarshal(r.AdapterConfig.Value); err != nil {
			log.Errorf("error unmarshalling adapter config: %v", err)
			return nil, err
		}
	}

	decodeValue := func(in interface{}) interface{} {
		switch t := in.(type) {
		case *policy.Value_StringValue:
			return t.StringValue
		case *policy.Value_Int64Value:
			return t.Int64Value
		case *policy.Value_DoubleValue:
			return t.DoubleValue
		default:
			return fmt.Sprintf("%v", in)
		}
	}

	decodeValueMap := func(in map[string]*policy.Value) map[string]interface{} {
		out := make(map[string]interface{}, len(in))
		for k, v := range in {
			out[k] = decodeValue(v.GetValue())
		}
		return out
	}

	props := decodeValueMap(r.Instance.Subject.Properties)
    tokenKey := fmt.Sprint(cfg.AuthKey)

	for k, v := range props {
		tokenString := fmt.Sprint(v)
		if (k == "custom_token_header") && strings.Contains(tokenString, tokenKey) {
            tokenString = strings.Replace(tokenString, "Bearer ", "", -1)
			token, _, err := new(jwt.Parser).ParseUnverified(tokenString, jwt.MapClaims{})
			if err != nil {
				fmt.Println(err)
				return nil, nil
			}
			log.Infof("valid JWT")
			if claims, ok := token.Claims.(jwt.MapClaims); ok {
				tokenScope := fmt.Sprint(claims["scope"])
				log.Infof("Scope: ", tokenScope)
				if tokenScope == "Doctor" {
					log.Infof("user is a Doctor, perform checks...")
                    now := time.Now()
                    hr, _, _ := now.Clock()
                    parsedHr := fmt.Sprint(hr)
                    log.Infof("current hour is: ", parsedHr)
					if hr >= 9 && hr < 17 {
						log.Infof("success, inside of work hours!!")
						return &v1beta1.CheckResult{
							Status: status.OK,
						}, nil
					}
					log.Infof("failure; outside of work hours!!")
					return &v1beta1.CheckResult{
						Status: status.WithPermissionDenied("Unauthorized..."),
					}, nil
				}
			} else {
				log.Infof("failure; invalid token claims!!")
					return &v1beta1.CheckResult{
						Status: status.WithPermissionDenied("Unauthorized..."),
					}, nil
			}
			log.Infof("success, as you're not a doctor!!")
			return &v1beta1.CheckResult{
				Status: status.OK,
			}, nil
		}
	}
	log.Infof("success, allow access to frontend and utils backend")
	return &v1beta1.CheckResult{
		Status: status.OK,
	}, nil
}

// Addr returns the listening address of the server
func (s *MyGrpcAdapter) Addr() string {
	return s.listener.Addr().String()
}

// Run starts the server run
func (s *MyGrpcAdapter) Run(shutdown chan error) {
	shutdown <- s.server.Serve(s.listener)
}

// Close gracefully shuts down the server; used for testing
func (s *MyGrpcAdapter) Close() error {
	if s.server != nil {
		s.server.GracefulStop()
	}

	if s.listener != nil {
		_ = s.listener.Close()
	}

	return nil
}

// NewMyGrpcAdapter creates a new IBP adapter that listens at provided port.
func NewMyGrpcAdapter(addr string) (Server, error) {
	if addr == "" {
		addr = "0"
	}
	listener, err := net.Listen("tcp", fmt.Sprintf(":%s", addr))
	if err != nil {
		return nil, fmt.Errorf("unable to listen on socket: %v", err)
	}
	s := &MyGrpcAdapter{
		listener: listener,
	}
	fmt.Printf("listening on \"%v\"\n", s.Addr())
	s.server = grpc.NewServer()
	authorization.RegisterHandleAuthorizationServiceServer(s.server, s)
	return s, nil
}
