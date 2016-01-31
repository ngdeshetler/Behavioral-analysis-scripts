subs={'661','662','663','664','665','666','667','668','669','670'};

for sub=1:length(subs)
cd(['~/Box Sync/data_drop/' subs{sub}]) 
v=dir('*test.mat');
load(v.name)
b=[theData.image_test];
names=fieldnames(b);
for n=1:length(names)
c.(names{n})={b.(names{n})};
c.(names{n})=cat(1,c.(names{n}){:});
end
save('R_data.mat','-struct','c')
end