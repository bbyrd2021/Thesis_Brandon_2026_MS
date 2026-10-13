$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
$xdvipdfmx = 'xdvipdfmx -E -o %D %O %S';
# Preserve XeLaTeX/fontspec when a client explicitly requests a -pdf build.
# Separate XDV generation from PDF conversion (avoids an older renderer pipe crash).
$pdflatex = 'xelatex -no-pdf -interaction=nonstopmode -halt-on-error %O %S && xdvipdfmx -E -o %Z%R.pdf %Y%R.xdv';
