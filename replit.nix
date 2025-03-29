{pkgs}: {
  deps = [
    pkgs.nodejs
    pkgs.openssl_1_1
    pkgs.chromium
    pkgs.geckodriver
    pkgs.imagemagick
    pkgs.postgresql
    pkgs.openssl
  ];
}
