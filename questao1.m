format long e
realmax
realmin
eps

format long e

xs = [1e-15, 1e15];
f_true = 1;

for x = xs
    f_aprox = ((1 + x) - 1) / x;

    erro_abs = abs(f_true - f_aprox);
    erro_rel = erro_abs / abs(f_true);

    fprintf('\n=== x = %.1e ===\n', x);
    fprintf('f_aprox     = %.16e\n', f_aprox);
    fprintf('Erro abs    = %.16e\n', erro_abs);
    fprintf('Erro rel    = %.16e\n', erro_rel);
end

xv = logspace(-20, 0, 400);
fv = ((1 + xv) - 1) ./ xv;

semilogx(xv, fv, 'LineWidth', 2)
grid on
xlabel('x')
ylabel('((1+x)-1)/x')
title('Efeito de ponto flutuante e cancelamento em ((1+x)-1)/x')

xs = [1e-15, 1e15];
for x = xs
    f_ruim = ((1+x)-1)/x;
    f_boa  = 1;

    fprintf('x=%.1e | ruim=%.16e | boa=%.16e | diff=%.3e\n', ...
        x, f_ruim, f_boa, abs(f_ruim - f_boa));
end