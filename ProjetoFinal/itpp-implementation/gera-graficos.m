#!/usr/bin/env octave-cli

1;

bpsk = csvread('bpsk.csv');
rs = csvread('rs.csv');
cc = csvread('cc.csv');
semilogy(bpsk(:,2), bpsk(:,1), "linewidth", 3, rs(:,2), rs(:,1), "linewidth", 3, cc(:,2), cc(:,1), "linewidth", 3)
grid on;
ylabel("Probabilidade de erro");
xlabel("Eb/N0 (dB)");
title("BER simulado");
legend("BPSK AWGN", "RS (7,4)", "CC (R=.5,K=7)");
print('output.jpg', "-S1200,900")
