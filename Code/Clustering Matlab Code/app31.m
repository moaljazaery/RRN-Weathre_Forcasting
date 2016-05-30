clc;
clear;
close all;

data=load('Locations');
X=data;
X.Locations
k=20;                        % The number of clusters

[IDX, C]=kmeans(X.Locations,k);

Colors=hsv(k);
for i=1:k
    Xi=X.Locations(IDX==i,:);
    plot(Xi(:,1),Xi(:,2),'o','MarkerSize',10,'Color',Colors(i,:));
    hold on;
    plot(C(i,1),C(i,2),'ks','MarkerSize',12,'MarkerFaceColor',Colors(i,:));
end

xlswrite('My_file.xls',IDX,'Sheet1','B2');

