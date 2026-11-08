#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript R/run_analysis.R path/to/gbd_harmonised.csv")
input <- args[[1]]
suppressPackageStartupMessages({library(readr); library(dplyr); library(ggplot2); library(tidyr)})
required <- c("measure","location","year","sex","age","cause","metric","value","lower","upper")
dat <- read_csv(input, show_col_types = FALSE)
missing <- setdiff(required, names(dat))
if (length(missing)) stop(paste("Missing columns:", paste(missing, collapse=", ")))
if (any(is.na(dat$value) | is.na(dat$lower) | is.na(dat$upper))) stop("Missing numeric estimates")
if (any(dat$lower > dat$value | dat$value > dat$upper)) stop("Invalid uncertainty interval order")
if (any(dat$value < 0 | dat$lower < 0 | dat$upper < 0)) stop("Negative estimates detected")
dir.create("results/tables", recursive=TRUE, showWarnings=FALSE)
dir.create("results/figures", recursive=TRUE, showWarnings=FALSE)
endpoint <- dat %>% group_by(measure,location,sex,age,cause,metric) %>% arrange(year,.by_group=TRUE) %>% filter(n()>=2) %>% summarise(start_year=first(year),end_year=last(year),start_value=first(value),end_value=last(value),absolute_change=end_value-start_value,relative_change_pct=ifelse(start_value==0,NA_real_,(end_value/start_value-1)*100),.groups="drop")
write_csv(endpoint,"results/tables/R_endpoint_changes.csv")
plotdat <- dat %>% filter(location=="Nigeria",measure %in% c("DALYs","YLLs","YLDs"),tolower(metric)=="rate")
if(nrow(plotdat)){p<-ggplot(plotdat,aes(year,value,colour=cause,fill=cause))+geom_ribbon(aes(ymin=lower,ymax=upper),alpha=.10,colour=NA)+geom_line(linewidth=.7)+facet_wrap(~measure,scales="free_y")+labs(title="Nigeria: burden rates over time",x="Year",y="Rate (source-defined units)")+theme_minimal(base_size=11)+theme(legend.position="bottom");ggsave("results/figures/R_nigeria_burden_trends.png",p,width=11,height=7,dpi=300)}
message("R analysis completed. Confirm source hierarchy, units and age-standardisation before interpretation.")
