# _*_ coding: UTF-8 _*_

from rpy2.robjects import r

#线性回归
def def_lm(X, Y, method='无'):
    r('''def_lm <- function(X,Y,method='无'){
          X <- as.data.frame(X)
          Y <- as.data.frame(Y)
          df <- cbind(X,Y)
          n <- ncol(X)
          name_list <- colnames(X)
          name_y <- colnames(Y)
          l <- paste(name_y,name_list[1],sep=' ~ ')
          if (n>1){
            for(i in 2:n){
              l = paste(l,name_list[i],sep = "+")
            }
          }

          library(MASS)
          l = formula(l)
          if (method == '无'){
            model <- lm(l,data = df)
          }
          else{
            model <- lm(l,data = df)
            model <- stepAIC(model,direction = method)
          }
          summary <- summary(model)  
          confint <- confint(model) 
          fitted <- model$fitted.values 
          resid <- residuals(model)  
          library(car)
          if (nrow(summary$coefficients) - 1 > 1){
            vif <- sqrt(vif(model))
          }
          else{
            vif <- '模型中仅剩下一个变量，无法计算VIF'
          }
          ncv <- ncvTest(model) 
          db <- durbinWatsonTest(model) 
          outlier <- outlierTest(model) 
          return(list(summary,confint,fitted,resid,vif,ncv,db,outlier))
    }''')
    res = r.def_lm(X, Y, method)
    return res

#多项式回归
def def_PolReg(X, Y, max, method):
    r('''def_PolReg <- function(X,Y,max,method){
          X <- as.data.frame(X)
          Y <- as.data.frame(Y)
          for (i in 2:max){
            X_plus <- as.data.frame(X[1] ** i)
            X <- cbind(X,X_plus)
            names_plus <- paste(colnames(X)[1],i,sep='')
            colnames(X)[ncol(X)] <- names_plus
          }
          df <- cbind(X,Y)
          
          n <- ncol(X)
          name_list <- colnames(X)
          name_y <- colnames(Y)
          l <- paste(name_y,name_list[1],sep=' ~ ')
          if (n>1){
            for(i in 2:n){
              l = paste(l,name_list[i],sep = "+")
            }
          }
          
          library(MASS)
          l = formula(l)
          if (method == '无'){
            model <- lm(l,data = df)
          }
          else{
            model <- lm(l,data = df)
            model <- stepAIC(model,direction = method)
          }
          summary <- summary(model)  
          confint <- confint(model) 
          fitted <- model$fitted.values 
          resid <- residuals(model) 
          library(car)
          if (nrow(summary$coefficients) - 1 > 1){
            vif <- sqrt(vif(model))
          }
          else{
            vif <- '模型中仅剩下一个变量，无法计算VIF'
          }
          ncv <- ncvTest(model) 
          db <- durbinWatsonTest(model) 
          outlier <- outlierTest(model)
          return(list(summary,confint,fitted,resid,vif,ncv,db,outlier))
    }''')
    res = r.def_PolReg(X, Y, max, method)

    return res

#逻辑回归
def def_logit(X, Y, method):
    r('''def_logit <- function(X,Y,method="both"){
          # X：a data frame or a matrix; Y:a data frame or a list
          # direction = c("both", "backward", "forward")
          X <- as.data.frame(X)
          Y <- as.data.frame(Y)
          df <- cbind(X,Y)
          n <- ncol(X)
          name_list <- colnames(X)
          name_y <- colnames(Y)
          l <- paste(name_y,name_list[1],sep=' ~ ')
          if (n>1){
            for(i in 2:n){
              l = paste(l,name_list[i],sep = "+")
            }
          }
          
          library(MASS)
          l = formula(l)
          if (method == '无'){
            model <- lm(l,data = df)
          }
          else{
            model <- lm(l,data = df)
            model <- stepAIC(model,direction = method)
          }
          summary <- summary(model)
          confint <- confint(model)
          fitted <- model$fitted.values
          resid <- residuals(model)
          library(car)
          if (nrow(summary$coefficients) - 1 > 1){
            vif <- sqrt(vif(model))
          }
          else{
            vif <- '模型中仅剩下一个变量，无法计算VIF'
          }
          ncv <- ncvTest(model) 
          db <- durbinWatsonTest(model) 
          outlier <- outlierTest(model) 
          return(list(summary,confint,fitted,resid,vif,ncv,db,outlier))
    }''')
    res = r.def_logit(X, Y, method)

    return res

#非线性回归
def def_nonlinear(x, y, formula, start):
    r('''def_nonlinear <- function(x,y,formula,start){
            dataset <- cbind(x,y)
            model <- nls(formula,data = dataset,start = start)
            return(summary(model))
    }''')
    res = r.def_nonlinear(x, y, formula, start)

    return res
