curl 'https://localhost:5000/v1/uudex/datasets' \
    --header "Content-Type: application/json" \
    --key "/home/d3m614/repos/UUDEX/example_ssl_certs/client/client.key" \
    --cert "/home/d3m614/repos/UUDEX/example_ssl_certs/client/client.crt" \
    --cacert "/home/d3m614/repos/UUDEX/example_ssl_certs/ca.pem"