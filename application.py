from flask import Flask,render_template,request
import pandas as pd
from pandasai import SmartDataframe as smartdf
from pandasai.llm.openai import OpenAI
import matplotlib
import japanize_matplotlib
import os
from datetime import datetime as dt
matplotlib.use('Agg')


# your api key
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# OpenAIのllmインスタンス
llm = OpenAI(api_token=OPENAI_API_KEY, model="gpt-4-1106-preview")
# PandasAIインスタンス
df = pd.read_csv('static/sample_data.csv')
dfHtml = df.to_html(classes='my-table')
full_path = 'static/'

config = {
    "save_charts":True,
    "save_charts_path":full_path,
    "llm": llm,
    "enable_cache": False,
    "verbose":True
    }

pandas_ai = smartdf(df, config=config)
resultElements = []

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    print("request method:", request.method)
    if request.method == 'GET':
        return render_template("page.html",dataTable = dfHtml, result="<div></div>")
    elif request.method == 'POST':
        query = request.form["query"]
        answer = pandas_ai.chat(query+"画像の場合はtemp_chart.pngとして保存して下さい。")


        if type(answer) is str and 'png' in answer:
            print("answer image:", answer)
            # listPngs = glob.glob('static/*.png')
            # latest_file = max(listPngs, key=os.path.getctime)
            # div = f"<img src = '{latest_file}'>"
            div = f"<img src = '{answer}' width='500' height='400'>"
        
        elif type(answer) is str or type(answer) is int:
            div = f'<div>{str(answer)}</div>'

        elif type(answer) is smartdf:
            dfHtmlResult = answer.to_html(classes='my-table')
            div = dfHtmlResult
        
        resultElements.append(f"<h4>Q: {query} {dt.now().strftime('%Y/%m/%d %H:%M')}</h4>")
        resultElements.append(div)
        print("resultList:",resultElements)
        return render_template("page.html",dataTable = dfHtml, results=resultElements)

## 実行
if __name__ == "__main__":
    app.run(debug=True)
    
