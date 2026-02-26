clc; clear; close all;
format long e

a = 1 - 2e-8;
b = 1 + 2e-8;
n = 401;

x = linspace(a, b, n);

% Forma expandida (como no enunciado)
f_expand = x.^7 ...
         - 7*x.^6 ...
         + 21*x.^5 ...
         - 35*x.^4 ...
         + 35*x.^3 ...
         - 21*x.^2 ...
         + 7*x ...
         - 1;

% Forma reescrita (mais estável)
f_estavel = (x - 1).^7;

% Diferença entre as formas
diff_abs = abs(f_expand - f_estavel);

fprintf('max |f_expand|  = %.3e\n', max(abs(f_expand)));
fprintf('max |f_estavel| = %.3e\n', max(abs(f_estavel)));
fprintf('max |dif|       = %.3e\n', max(diff_abs));

figure;
plot(x, f_expand, 'LineWidth', 1.5); hold on;
plot(x, f_estavel, '--', 'LineWidth', 1.5);
grid on;
xlabel('x');
ylabel('f(x)');
title('f(x) - Forma Expandida vs (x-1)^7');
legend('Expandida', '(x-1)^7', 'Location', 'best');

tiny = realmin;

figure;
semilogy(x, abs(f_expand) + tiny, 'LineWidth', 1.5); hold on;
semilogy(x, abs(f_estavel) + tiny, '--', 'LineWidth', 1.5);
grid on;
xlabel('x');
ylabel('|f(x)|');
title('|f(x)| em escala log');
legend('|Expandida|', '|(x-1)^7|', 'Location', 'best');

figure;
semilogy(x, diff_abs + tiny, 'LineWidth', 1.5);
grid on;
xlabel('x');
ylabel('|f_{expand} - f_{estavel}|');
title('Erro entre as duas formas');