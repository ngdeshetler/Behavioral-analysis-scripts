# -*- coding: utf-8 -*-
"""
This script should create a database for looking at the sequence project
"""
# Objects for Trials, Subjects, and Database
class Trial:
    trial_types={'1':'Mismatch', '2':'Repeat','3':'Scramble'}
    def __init__(self,trial_num,seq_ref,position,orig_pos,imge_ref,choice,cor,rt,trial_type,novell):
        self.num=trial_num
        self.seq=seq_ref
        self.place=position
        self.old_place=orig_pos
        self.img=imge_ref
        self.cor=cor
        self.corr=self.cor == '1'
        self.uncorr=self.cor == '0'
        self.rt=rt
        self.type=trial_type
        self.novell=novell
        self.novel=self.novell=='1'
    def status(self,correct=True,t_type='ns',pos='ns',novel=False,incorrect=False,non_novel=False):
        corr_bol=True
        if correct:
            corr_bol=self.corr
        elif incorrect:
            corr_bol=self.uncorr
        novel_bol=True
        if novel:
            novel_bol=self.novel
        elif non_novel:
            novel_bol=self.novel==False
        return (self.type==t_type or self.trial_types[self.type].lower()==t_type.lower() or t_type=='ns') and (self.place==pos or pos=='ns') and corr_bol and novel_bol
        
    
class Subject:
    positions=['2','3','4']
    trial_types=['Repeat','Mismatch','Scramble']
    def __init__(self,SID,trials_list):
        self.SID=SID
        self.trials=trials_list
        self.trial_count=len(trials_list)
    def append_trials(self,trial):
        self.trials.append(trial)
        self.trial_count=len(self.trials)
    def summary(self,status_type='count',correct=True,weight=True,t_type='ns',pos='ns',novel=False,non_novel=False):
        if status_type=='count':
            if not correct and weight:
                print('Error: Can not weight when using all instances')
                return 
            if weight:
                return float(sum(1 for trial in self.trials if trial.status(correct,t_type,pos,novel,False,non_novel)))/\
                max(1,sum(1 for trial in self.trials if trial.status(False,t_type,pos,novel,False,non_novel)))
            else:
                return sum(1 for trial in self.trials if trial.status(correct,t_type,pos,novel,non_novel))
        elif status_type=='rt':
            return float(sum(float(trial.rt) for trial in self.trials if trial.status(correct,t_type,pos,novel,non_novel)))/\
            max(1,sum(1 for trial in self.trials if trial.status(correct,t_type,pos,novel,non_novel)))
    def return_row(self,status_type='count',total=True,total_per=True,novels=True,t_types=True,type_novel=True,poss=False,type_pos=True,type_pos_novel=True):
        return_list=[self.SID]
        if total:
            return_list.append(self.summary(status_type=status_type,weight=False))
        if total_per:
            return_list.append(self.summary(status_type=status_type))
        if novels:
            return_list.append(self.summary(status_type=status_type,novel=True))
        if t_types:
            for ttype in self.trial_types:
                return_list.append(self.summary(status_type=status_type,t_type=ttype))
        if type_novel:
            for ttype in self.trial_types:
                return_list.append(self.summary(status_type=status_type,t_type=ttype,novel=True))
        if poss:
            for poses in self.positions:
                return_list.append(self.summary(status_type=status_type,pos=poses))
        if type_pos:
            for ttype in self.trial_types:
                for poses in self.positions:
                    return_list.append(self.summary(status_type=status_type,t_type=ttype,pos=poses,non_novel=True))
        if type_pos_novel:
            for ttype in self.trial_types:
                for poses in self.positions:
                    return_list.append(self.summary(status_type=status_type,t_type=ttype,pos=poses,novel=True))
        return return_list
    def print_row(self,status_type='count',total=True,total_per=True,novels=True,t_types=True,type_novel=True,poss=False,type_pos=True,type_pos_novel=True):
        print_list=self.return_row(status_type,total,total_per,novels,t_types,type_novel,poss,type_pos,type_pos_novel)
        for item in print_list:
            print ('%.3f ' % item),
    def return_row_titles(self,total=True,total_per=True,novels=True,t_types=True,type_novel=True,poss=False,type_pos=True,type_pos_novel=True):
        return_list=['SID']
        if total:
            return_list.append('Total_correct')
        if total_per:
            return_list.append('%_correct')
        if novels:
            return_list.append('Novels')
        if t_types:
            for ttype in self.trial_types:
                return_list.append(ttype)
        if type_novel:
            for ttype in self.trial_types:
                return_list.append(ttype + '_novel')
        if poss:
            for poses in self.positions:
                return_list.append('Position_' + poses)
        if type_pos:
            for ttype in self.trial_types:
                for poses in self.positions:
                    return_list.append((ttype + '_' + poses + '_nonNovel'))
        if type_pos_novel:
            for ttype in self.trial_types:
                for poses in self.positions:
                    return_list.append((ttype + '_' + poses + '_novel'))
        return return_list
    def print_row_titles(self,total=True,total_per=True,novels=True,t_types=True,type_novel=True,poss=False,type_pos=True,type_pos_novel=True):
        print_list=self.return_row_titles(total,total_per,t_types,poss,type_pos)
        for item in print_list:
            print(item),
                    
class Dataset:
    def __init__(self,subject_list):
        self.subjects=subject_list
        self.n=len(subject_list)
    def group_ave(self,status_type='count',correct=True,weight=True,t_type='ns',pos='ns',novel=False):
        return sum(sub.summary(status_type,correct,weight,t_type,pos,novel) for sub in self.subjects)/self.n
    def group_list(self,status_type='count',correct=True,weight=True,t_type='ns',pos='ns',novel=False):
        return_list=[]
        for sub in self.subjects:
            return_list.append(sub.summary(status_type,correct,weight,t_type,pos,novel))
        return return_list
    def ttest(self,conditions1,conditions2):
        from scipy import stats
        stats.ttest_ind(self.group_list(*conditions1),self.group_list(*conditions2))
    def export_data(self,save_file,status_type='count',total=True,total_per=True,novels=True,t_types=True,type_novel=True,poss=False,type_pos=True,type_pos_novel=True):
        import csv
        with open(save_file,'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow(self.subjects[0].return_row_titles(total,total_per,novels,t_types,type_novel,poss,type_pos,type_pos_novel))
            a.writerows(sub.return_row(status_type,total,total_per,novels,t_types,type_novel,poss,type_pos,type_pos_novel) for sub in self.subjects)
    
## Need to be in directory, need to gte txt_file
import os
import time
from datetime import date

base_dir=os.path.dirname(os.path.realpath(__file__))    
#    '/601/601_data_test_02-Oct-2015_12:19:12.txt',
#    '/602/602_data_test_02-Oct-2015_15:24:16.txt',
#    '/603/603_data_test_02-Oct-2015_16:20:41.txt',
#    '/604/604_data_test_06-Oct-2015_16:16:24.txt',
#    '/605/605_data_test_06-Oct-2015_14:30:12.txt',
#    '/606/606_data_test_06-Oct-2015_15:28:14.txt',
#    '/607/607_data_test_07-Oct-2015_12:28:36.txt',
#    '/608/608_data_test_08-Oct-2015_17:29:48.txt',
#    '/609/609_data_test_08-Oct-2015_14:29:50.txt',
#    '/610/610_data_test_09-Oct-2015_13:55:44.txt',
#    '/611/611_data_test_13-Oct-2015_14:24:28.txt',
#    '/612/612_data_test_13-Oct-2015_15:32:16.txt',
#    '/613/613_data_test_15-Oct-2015_14:27:39.txt',
#    '/614/614_data_test_16-Oct-2015_13:55:55.txt',
#    '/615/615_data_test_16-Oct-2015_13:06:20.txt',
#    '/616/616_data_test_20-Oct-2015_14:33:15.txt',
txt_files=[
    '/627/627_data_test_06-Nov-2015_08:53:15.txt',
    '/628/628_data_test_05-Nov-2015_22:56:07.txt',
    '/629/629_data_test_06-Nov-2015_08:54:07.txt',
    '/630/630_data_test_06-Nov-2015_08:54:48.txt',
    '/631/631_data_test_06-Nov-2015_14:34:33.txt',
    '/632/632_data_test_06-Nov-2015_14:34:57.txt',
    '/633/633_data_test_10-Nov-2015_15:33:50.txt',
    '/634/634_data_test_13-Nov-2015_13:05:11.txt',
    '/635/635_data_test_13-Nov-2015_14:07:34.txt',
    '/636/636_data_test_13-Nov-2015_08:27:28.txt',
    '/637/637_data_test_17-Nov-2015_16:27:44.txt',
    '/638/638_data_test_17-Nov-2015_15:50:31.txt',
    '/639/639_data_test_17-Nov-2015_14:28:20.txt',
    '/640/640_data_test_18-Nov-2015_12:33:08.txt',
    '/641/641_data_test_19-Nov-2015_16:35:06.txt',
    '/642/642_data_test_20-Nov-2015_08:00:29.txt',
    '/643/643_data_test_01-Dec-2015_15:29:49.txt',
    '/644/644_data_test_02-Dec-2015_12:33:16.txt',
    '/645/645_data_test_07-Jan-2016_16:01:23.txt',
    '/646/646_data_test_07-Jan-2016_12:42:08.txt',
    '/647/647_data_test_08-Jan-2016_11:53:05.txt',
    '/648/648_data_test_08-Jan-2016_13:16:11.txt',
    '/649/649_data_test_12-Jan-2016_13:06:24.txt',
    '/650/650_data_test_12-Jan-2016_16:31:05.txt',
    '/651/651_data_test_12-Jan-2016_15:28:56.txt',
    '/652/652_data_test_13-Jan-2016_09:58:26.txt',
    '/653/653_data_test_14-Jan-2016_12:56:04.txt',
    '/654/654_data_test_14-Jan-2016_15:57:22.txt',
    '/655/655_data_test_15-Jan-2016_12:52:35.txt',
    '/656/656_data_test_15-Jan-2016_10:02:29.txt',
    '/657/657_data_test_15-Jan-2016_11:56:59.txt',
    '/658/658_data_test_20-Jan-2016_09:56:22.txt',
    '/659/659_data_test_21-Jan-2016_13:12:30.txt'
    ]
#subj_IDs=['601','602','603','604','605','606','607','608','609','610','611','612','613','614','615','616']
subj_IDs=['627','628','629','630','631','632','633','634','635','636','637',\
'638','639','640','641','642','643','644','645','646','647','648','649','650','651',\
'652','653','654','656','657','658','659']
subjects=[]

for index, sub in enumerate(subj_IDs):
    text_file=open((str(base_dir) + txt_files[index]),'r')
    rows=text_file.read().split('\n')#gets all the rows from the text file
    
    subject=Subject(sub,[])            

    for row in range(2,len(rows)):
        working_row=rows[row].split('\t')
        if len(working_row)==10:
            subject.append_trials(Trial(*working_row))
    subjects.append(subject)

data=Dataset(subjects)
data.export_data((base_dir + '/subject_sum_'+ time.strftime("%d-%m-%Y") +'.csv'))
data.export_data((base_dir + '/subject_sum_'+ time.strftime("%d-%m-%Y") +'_RT.csv'),status_type='rt')
