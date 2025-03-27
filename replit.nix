{pkgs}: {
  deps = [
    pkgs.chromium
    pkgs.geckodriver
    pkgs.imagemagick
    pkgs.postgresql
    pkgs.openssl
  ];
}
