import subprocess

# -- client -------------------------------------------------------------- #

# 例：メモ帳を起動する
def c_notepad():
    return ...


# -- host ---------------------------------------------------------------- #

# 例：メモ帳を起動する
@app.route("/function/test_common/notepad", methods=["GET"])
def h_notepad():
    subprocess.run(['notepad.exe'])
    param = request.args.get('param')
    
    # ここで必要な処理を行い、結果を生成する
    result = {'received_param': param, 'message': 'Hello, World!'}
    
    # 結果をJSON形式で返す
    return jsonify(result)

