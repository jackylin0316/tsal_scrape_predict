
from utils.scrape import get
from predict import today_price

if __name__=='__main__':
    df=get()
    df.to_csv('./utils/tsla_history.csv', index=False)
    print('Saved to csv file')

    today=today_price()
    print(f'Today TSLA stock price is : {today}')
    
