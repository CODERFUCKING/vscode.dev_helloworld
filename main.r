library(stringr)

KOR_stock = read.csv('data/KOR_stock.csv', row.names = 1, stringsAsFactors = FALSE)
KOR_sector = read.csv('data/KOR_sector.csv', row.names = 1, stringsAsFactors = FALSE)

KOR_stock$'종목코드' = str_pad(KOR_stock$'종목코드', 6,'left', 0)
KOR_sector$'CMP_CD' = str_pad(KOR_sector$'CMP_CD', 6, 'left', 0)

# 종목코드 크롤링 값에 대해서 변수값으로 설정해서 불어오기

data_market = left_join(KOR_ticker, KOR_sector, by = c('종목코드' = 'CMP_CD', '종목명' = 'CMP_KOR'))

head(data_market)

