from flask import Flask,render_template,request
import pandas as pd
from pandasai import SmartDataframe as smartdf
from pandasai.llm.openai import OpenAI
import matplotlib
matplotlib.use('Agg')


# your api key
api_key = "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" # 木村で発行した私用のopenai APIキー
OPENAI_API_KEY = api_key
# OpenAIのllmインスタンス
llm = OpenAI(api_token=OPENAI_API_KEY)
# PandasAIインスタンス
df = pd.DataFrame({"拠点":["拠点1","拠点2","拠点3"], "人数":[3,4,5], "電気":["停電有り", "停電無し", "調査中"]})
dfHtml = df.to_html(classes='my-table')
full_path = 'static/'

config = {"save_charts":True, "save_charts_path":full_path, "llm": llm, "enable_cache": False}

pandas_ai = smartdf(df, config=config)


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    print("request method:", request.method)

    if request.method == 'GET':
        return render_template("page.html",dataTable = dfHtml, result="<div></div>")
    elif request.method == 'POST':
        query = request.form["query"]
        answer = pandas_ai.chat(query+"画像の場合はtemp_chart.pngとして保存して下さい。")

        if type(answer) is str or type(answer) is int:
            div = f'<div>{str(answer)}</div>'
        elif type(answer) is smartdf:
            div = f'<div>{str(answer)}</div>'
        else:
            print("answer image:", answer)
            div = "<img src = f'{full_path}temp_chart.png'></div>"

        return render_template("page.html",dataTable = dfHtml, result=div)

## 実行
if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(e)
