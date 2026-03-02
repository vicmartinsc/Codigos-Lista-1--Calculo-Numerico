%% QUESTAO 1 - CALCULO NUMERICO (Lista 1)
% Objetivos desta questão:
%  (1) Mostrar realmax, realmin e eps (double) e explicar o significado
%  (2) Avaliar numericamente a expressão ((1+x)-1)/x para x = 1e-15 e 1e15
%  (3) Calcular erros absoluto e relativo em relação ao valor exato (=1)
%  (4) Discutir a diferença dos resultados (efeitos de ponto flutuante)

clc; clear; close all;
format long e

%% #RealmaxRealminEps
% Em ponto flutuante (double), existem limites de representação:
% - realmax: maior número finito representável (acima disso -> overflow -> Inf)
% - realmin: menor número positivo normalizado representável (abaixo disso -> underflow)
% - eps: menor incremento tal que 1 + eps != 1 (mede a resolução perto de 1)

fprintf('========================\n');
fprintf(' #RealmaxRealminEps\n');
fprintf('========================\n');

rmx = realmax;
rmn = realmin;
ep  = eps;

fprintf('realmax = %.16e\n', rmx);
fprintf('realmin = %.16e\n', rmn);
fprintf('eps     = %.16e\n', ep);


%% #InterpretacaoDosValores
fprintf('\n========================\n');
fprintf(' #InterpretacaoDosValores\n');
fprintf('========================\n');

fprintf(['Interpretacao:\n',...
    '- realmax: maior numero finito representavel em double. Se ultrapassar -> Inf (overflow).\n',...
    '- realmin: menor numero positivo normalizado em double. Abaixo disso tende a ir para 0 (underflow).\n',...
    '- eps: menor numero tal que 1 + eps eh diferente de 1 (resolucao numerica perto do 1).\n']);

% Ideia-chave:
% "eps" indica a escala de erro relativo mínimo típico em operações.
% Se um numero for pequeno demais comparado ao espaçamento local dos doubles,
% ele pode nao alterar o resultado de uma soma (ex.: 1 + x pode virar 1).

%% #DefinicaoDaExpressao
% A expressão pedida:
%   f(x) = ((1 + x) - 1) / x
%
% Matematicamente, (1+x) - 1 = x, então:
%   f(x) = x/x = 1  (valor EXATO)
%
% Porém, no computador, (1+x) pode arredondar para 1 quando x é muito pequeno,
% e ao fazer (1+x)-1 ocorre cancelamento, gerando perda de precisão.

fprintf('\n========================\n');
fprintf(' #DefinicaoDaExpressao\n');
fprintf('========================\n');

f_true = 1; % valor exato (matematicamente)

fprintf('Valor exato (matematico) de f(x) = 1\n');

%% #AvaliacaoDaExpressao
fprintf('\n========================\n');
fprintf(' #AvaliacaoDaExpressao\n');
fprintf('========================\n');

xs = [1e-15, 1e15];

% Vamos calcular f(x) para os dois casos pedidos:
for x = xs
    f_aprox = ((1 + x) - 1) / x;
    fprintf('x = %.1e  -> f_aprox = %.16e\n', x, f_aprox);
end

%% #ErroAbsolutoERelativo
% Definições:
% - erro absoluto: |f_true - f_aprox|
% - erro relativo: |f_true - f_aprox| / |f_true|
%
% Como f_true = 1, aqui o erro relativo = erro absoluto numericamente,
% mas a gente calcula do jeito geral para ficar "correto" e reutilizável.

fprintf('\n========================\n');
fprintf(' #ErroAbsolutoERelativo\n');
fprintf('========================\n');

for x = xs
    f_aprox = ((1 + x) - 1) / x;

    erro_abs = abs(f_true - f_aprox);
    erro_rel = erro_abs / abs(f_true);

    fprintf('\n--- Para x = %.1e ---\n', x);
    fprintf('f_aprox      = %.16e\n', f_aprox);
    fprintf('Erro absoluto= %.16e\n', erro_abs);
    fprintf('Erro relativo= %.16e\n', erro_rel);
end

%% #CancelamentoCatastrofico
% Para x muito pequeno (ex.: 1e-15):
% - O número 1 é representado com certa precisão.
% - Existe um espaçamento entre números representáveis perto de 1.
% - Se x for menor que esse espaçamento efetivo, a soma 1 + x pode "não mudar"
%   por arredondamento: (1 + x) vira exatamente 1 no computador.
% - Então (1 + x) - 1 vira 0.
% - E f(x) = 0/x = 0.
%
% Isso é chamado de CANCELAMENTO CATASTRÓFICO:
% subtrair dois números quase iguais "apaga" dígitos significativos e piora a precisão.

fprintf('\n========================\n');
fprintf(' #CancelamentoCatastrofico\n');
fprintf('========================\n');

x_small = 1e-15;
soma_small = 1 + x_small;
sub_small  = soma_small - 1;
f_small    = sub_small / x_small;

fprintf('Para x pequeno:\n');
fprintf('x            = %.1e\n', x_small);
fprintf('1 + x        = %.16e\n', soma_small);
fprintf('(1 + x) - 1  = %.16e\n', sub_small);
fprintf('f(x)         = %.16e\n', f_small);

fprintf(['\nComentario:\n',...
    'Se 1 + x arredonda para 1, entao (1+x)-1 = 0 e f(x)=0.\n',...
    'Isso mostra perda de precisao por cancelamento (subtracao de numeros quase iguais).\n']);

%% #EscalaNumerica
% Para x muito grande (ex.: 1e15):
% - O termo "1" é muito pequeno comparado a x.
% - 1 + x ~ x (numericamente).
% - Mas aqui isso não gera o mesmo tipo de problema de cancelamento no final,
%   e a razão tende a ficar próxima de 1.
%
% O ponto principal é: a qualidade numérica depende da escala de x e das operações.

fprintf('\n========================\n');
fprintf(' #EscalaNumerica\n');
fprintf('========================\n');

x_big = 1e15;
soma_big = 1 + x_big;
sub_big  = soma_big - 1;
f_big    = sub_big / x_big;

fprintf('Para x grande:\n');
fprintf('x            = %.1e\n', x_big);
fprintf('1 + x        = %.16e\n', soma_big);
fprintf('(1 + x) - 1  = %.16e\n', sub_big);
fprintf('f(x)         = %.16e\n', f_big);

fprintf(['\nComentario:\n',...
    'Aqui, 1 + x eh praticamente x, mas a expressao final tende a 1.\n',...
    'A diferenca entre os casos (x pequeno vs x grande) vem da aritmetica de ponto flutuante.\n']);

%% #ComparacaoDeFormas
% - Forma "original" (pode sofrer cancelamento): ((1+x)-1)/x
% - Forma "estável" (matematicamente equivalente): 1

fprintf('\n========================\n');
fprintf(' #ComparacaoDeFormas\n');
fprintf('========================\n');

for x = xs
    f_ruim = ((1 + x) - 1) / x;
    f_boa  = 1; % reescrita analitica (forma estavel)

    fprintf('x=%.1e | f_original=%.16e | f_estavel=%.16e | diff=%.3e\n', ...
        x, f_ruim, f_boa, abs(f_ruim - f_boa));
end

%% #VisualizacaoGrafica
% - Para x não tão pequeno, f(x) ~ 1
% - A partir de um certo ponto (x muito pequeno), aparecem desvios por limitações
%   do ponto flutuante e cancelamento.

fprintf('\n========================\n');
fprintf(' #VisualizacaoGrafica\n');
fprintf('========================\n');

xv = logspace(-20, 0, 400);           % 1e-20 ate 1
fv = ((1 + xv) - 1) ./ xv;

figure;
semilogx(xv, fv, 'LineWidth', 2);
grid on;
xlabel('x');
ylabel('((1+x)-1)/x');
title('Efeito de ponto flutuante em f(x)=((1+x)-1)/x');

% Opcional: também plotar o erro |1 - f(x)| em escala log:
figure;
semilogx(xv, abs(1 - fv), 'LineWidth', 2);
grid on;
xlabel('x');
ylabel('|1 - f(x)|');
title('Erro absoluto em f(x) ao variar x');

%% #Conclusao
% - realmax/realmin/eps caracterizam limites e precisao do double.
% - A expressao deveria dar 1, mas para x muito pequeno pode dar 0 (ou algo distante)
%   por arredondamento e cancelamento catastrófico.
% - Para x muito grande, o comportamento tende a ser melhor.
% - Reescrever expressões pode ser essencial para estabilidade numérica.

fprintf('\n========================\n');
fprintf(' #Conclusao\n');
fprintf('========================\n');

fprintf(['Conclusao:\n',...
    '- realmax/realmin/eps mostram limites e precisao do double.\n',...
    '- Para x pequeno, pode haver cancelamento e perda de precisao (resultado se afasta de 1).\n',...
    '- Para x grande, a expressao tende a ser mais bem comportada.\n',...
    '- Reescrita de formulas evita instabilidades numericas.\n']);