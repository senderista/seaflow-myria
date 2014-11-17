% script to show how seaflow data is binned wrt to the position of beads.
% Sophie Clayton, September 2014
% sclayton@uw.edu

% load in the data

mm_fsc = zeros(121,1);
mm_chl = zeros(121,1);
mm_pe = zeros(121,1);

bsize = 65520/60;
bins = -60:1:60;

%mm=zeros(121,121,121);
mm=zeros(121,121);
mmm=zeros(121,121);

% 
max_bin=zeros(length(Day),3);
min_bin=zeros(length(Day),3);

max_bin(:,1)=floor(new_fsc_max/bsize);
max_bin(:,2)=floor(new_chl_max/bsize);
max_bin(:,3)=floor(new_pe_max/bsize);
min_bin(:,1)=floor(new_fsc_min/bsize);
min_bin(:,2)=floor(new_chl_min/bsize);
min_bin(:,3)=floor(new_pe_min/bsize);

% for d=1:length(Day); % chl
% mm_fsc=mm_fsc(bins>=min_bin(d,1)&bins<=max_bin(d,1))+1;
% mm_chl=mm_chl(bins>=min_bin(d,2)&bins<=max_bin(d,2))+1;
% mm_pe=mm_pe(bins>=min_bin(d,3)&bins<=max_bin(d,3))+1;
% end
   
for d=1:length(Day);
    f = find(bins>=min_bin(d,1)&bins<=max_bin(d,1));
    c = find(bins>=min_bin(d,2)&bins<=max_bin(d,2));
    p = find(bins>=min_bin(d,3)&bins<=max_bin(d,3));
    mm(f,c)=mm(f,c)+1;
    mmm(f,p)=mm(f,p)+1;

end

figure;
bins_unit= -65520:bsize:65520;
pcolor(bins_unit,bins_unit,mm./47155);
shading flat
colormap default, cmap=colormap; colormap(cmap([8 10 10:58],:));
xlabel('fsc small')
ylabel('chl small')
box on

figure;
pcolor(bins_unit,bins_unit,mmm./47155);
shading flat
colormap default, cmap=colormap; colormap(cmap([8 10 10:58],:));
xlabel('fsc small')
ylabel('pe')
box on

