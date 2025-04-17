import io

def download_trade_log(trades_df):
    output = io.StringIO()
    trades_df.to_csv(output, index=False)
    return output.getvalue()
