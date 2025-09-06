# PowerShell script to generate self-signed SSL certificates
# This uses .NET's built-in certificate generation

$certPath = "nginx-selfsigned.crt"
$keyPath = "nginx-selfsigned.key"

# Create a self-signed certificate
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\LocalMachine\My" -NotAfter (Get-Date).AddDays(365)

# Export the certificate to PEM format
$certBytes = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
$certPem = "-----BEGIN CERTIFICATE-----`n"
$certPem += [System.Convert]::ToBase64String($certBytes, [System.Base64FormattingOptions]::InsertLineBreaks)
$certPem += "`n-----END CERTIFICATE-----"

# Export the private key to PEM format
$keyBytes = $cert.PrivateKey.ExportPkcs8PrivateKey()
$keyPem = "-----BEGIN PRIVATE KEY-----`n"
$keyPem += [System.Convert]::ToBase64String($keyBytes, [System.Base64FormattingOptions]::InsertLineBreaks)
$keyPem += "`n-----END PRIVATE KEY-----"

# Write the certificate and key to files
$certPem | Out-File -FilePath $certPath -Encoding ASCII
$keyPem | Out-File -FilePath $keyPath -Encoding ASCII

Write-Host "SSL certificates generated successfully!"
Write-Host "Certificate: $certPath"
Write-Host "Private Key: $keyPath"

# Clean up the certificate from the store
Remove-Item -Path "cert:\LocalMachine\My\$($cert.Thumbprint)" -Force
