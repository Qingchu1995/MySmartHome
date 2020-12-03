df = readtable('dht_rec.csv');
%%
figure;subplot(1,2,1);
plot(df.time(2:end),df.humidity(2:end));
grid on
ylabel('humidity (%)');
subplot(1,2,2);
plot(df.time(2:end),df.temperature(2:end));
grid on
ylabel('temperature (C)');