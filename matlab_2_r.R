install.packages("R.matlab")
subjects <- list()
subs <- c("661","662","663","664","665","666","667","668","669","670")

for(sub in subs){
temp_name=paste0("s", sub)
temp_data <- readMat(paste0("~/Box Sync/data_drop/",sub,"/R_data.mat"))
unclass(temp_data)
temp_data$weak.strong <- as.numeric(temp_data$weak.strong[sapply(temp_data$weak.strong,function(x) x=="1"|x=="4")])
subjects[[temp_name]] <- temp_data
}
