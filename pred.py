import numpy as np
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from math import log


def calc_pred(gp1, gp2, p, p2, label_col, split_col, defaults, h=1):
    ratio_prob = []
    direct_prob = []
    labels = []
    counter_p2_0 = 0
    counter_p0 = 0

    ods_mult_prob = []
    columns = list(gp1.columns)
    columns.remove(label_col)
    columns.remove(split_col)
    number_of_samples = 0
    ratio_bad = 0
    for index, row in gp2.iterrows():
        for c in columns:
            number_of_samples += 1
            key = (h, c, row[c])
            def_key = (h, c, defaults[c])
            if p2[def_key] == 0:
                counter_p2_0 += 1
                continue
            if p[def_key] == 0:
                counter_p0 += 1
                continue
            ratio_p = (p[key] / p[def_key]) * p2[def_key]
            if p[key] >= 1 or p2[key] >= 1:
                continue
            odds_1 = p[key] / (1 - p[key])
            if ratio_p > 1:
                ratio_bad += 1
                ratio_p = 0.999999
            direct_p = p[key]
            ratio_prob.append(ratio_p)
            direct_prob.append(direct_p)
            labels.append(row[label_col])

            odds_def1 = p[def_key] / (1 - p[def_key])
            odds_def2 = p2[def_key] / (1 - p2[def_key])
            mult_pred = odds_1 * odds_def2 / odds_def1
            ods_mult_prob.append(mult_pred / (1 + mult_pred))
            mul = mult_pred / (1 + mult_pred)

    return labels, direct_prob, ratio_prob, ods_mult_prob, ratio_bad, number_of_samples


def calc_loss(labels, direct_prob, ratio_prob, ods_mult_prob):
    direct_loss = 0
    ratio_loss = 0
    counter = 0
    error_cnt = 0
    mult_loss = 0
    for i in range(len(labels)):
        counter += 1

        try:
            direct = direct_prob[i]
            rat = ratio_prob[i]
            mult = ods_mult_prob[i]
            y = labels[i]
            l1 = -(y * log(direct) + (1 - y) * log(1 - direct))
            l2 = -(y * log(rat) + (1 - y) * log(1 - rat))
            l4 = -(y * log(mult) + (1 - y) * log(1 - mult))
            direct_loss += l1
            ratio_loss += l2
            mult_loss += l4
        except Exception as E:
            error_cnt += 1
            continue
    print("number of errors in calculating loss", error_cnt)
    return direct_loss/len(labels), ratio_loss/len(labels), mult_loss/len(labels)


def loss(y_test, preds):
    from math import log
    number_of_errors = 0
    loss = 0
    for i in range(len(y_test)):
        try:
            y = y_test[i]
            l = -(y * log(preds[i][1]) + (1-y)*log(1-preds[i][1]))
            loss += l
        except Exception as e:
            number_of_errors += 1
    res = loss/len(y_test)
    print("number of errors", number_of_errors, len(y_test), number_of_errors / len(y_test))

    return res, number_of_errors


def rat_models(preds,  p1_def_0, p1_def_1, p2_def_0, p2_def_1):
    val0 = p2_def_0 / p1_def_0
    val1 = p2_def_1 / p1_def_1
    ratio_preds = []
    odds_preds = []
    for row in preds:

        x0 = row[0] * val0
        x1 = row[1] * val1
        ratio_preds.append([x0, x1])

        odd0 = row[0] / (1-row[0])
        odd1 = row[1] / (1-row[1])
        odd1_def0 = p1_def_0 / (1-p1_def_0)
        odd1_def1 = p1_def_1 / (1-p1_def_1)
        odd2_def0 = p2_def_0 / (1-p2_def_0)
        odd2_def1 = p2_def_1 / (1-p2_def_1)

        oddpred0 = odd0 * odd2_def0 / odd1_def0
        oddpred1 = odd1 * odd2_def1 / odd1_def1
        podd0 = oddpred0 / (1+oddpred0)
        podd1 = oddpred1 / (1+oddpred1)
        odds_preds.append([podd0, podd1])
    ratio_preds = np.array(ratio_preds)
    odds_preds = np.array(odds_preds)
    return ratio_preds, odds_preds


def soph(gp1, gp2, label_col,  p1_def_0, p1_def_1, p2_def_0, p2_def_1):

    # Fit
    y_train = gp1[label_col].to_numpy()
    X_train = gp1.drop(columns=[label_col, 'ECOZONE']).to_numpy()
    y_test = gp2[label_col].to_numpy()
    X_test = gp2.drop(columns=[label_col, 'ECOZONE']).to_numpy()
    clf = LogisticRegression(random_state=0).fit(X_train, y_train)
    pred1 = clf.predict_proba(X_test)
    lrd, lrod = rat_models(pred1, p1_def_0, p1_def_1, p2_def_0, p2_def_1)

    xgb_cl = xgb.XGBClassifier()
    xgb_cl.fit(X_train, y_train)
    pred2 = xgb_cl.predict_proba(X_test)
    xgbd, xgbod = rat_models(pred2, p1_def_0, p1_def_1, p2_def_0, p2_def_1)

    l1 = loss(y_test, pred1)
    l2 = loss(y_test, lrd)
    l3 = loss(y_test, lrod)

    l4 = loss(y_test, pred2)
    l5 = loss(y_test, xgbd)
    l6 = loss(y_test, xgbod)

    return l1[0], l2[0], l3[0], l4[0], l5[0], l6[0]
