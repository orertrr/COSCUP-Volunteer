# 財務會計系統

COSCUP 目前是以**試算表**建立預算，在志工平台財務會計系統中**申請預算費用**。目標是可以完全將**財務組**的業務都移到志工平台上完成。

## 規劃流程圖

<figure markdown>
  <a href="https://s3.toomore.net/coscup/volunteer/docs_tasks_accounting_system.svg">
    <img alt="coscup_volunteer_infra" src="https://s3.toomore.net/coscup/volunteer/docs_tasks_accounting_system.svg">
  </a>
  <figcaption><small><a href="https://s3.toomore.net/coscup/volunteer/docs_tasks_accounting_system.svg">[original]</a></small></figcaption>
</figure>

## 流程解說

財務會計流程大致上會是這樣呈現，2022 年已經在志工平台上實作中間段「**費用申請**」的部分。預算表目前是用**匯入**試算表的方式建立項目。單據的部分目前無法**同時**與費用一起提交給財務組檢核。

### 政策設定

設置「科目編碼」在預算建立的時候也一併認列，目前預算還沒有與會計概念榜定在一起。

### 預算

每年的預算表大致上約有 80% 可以直接沿用前一年的項目，同項目可直接沿用前一年的參數建立。

!!! note "交通費補助"

    另外「交通費補助」（個人）看能不能在這裡也提列上去，或是將「交通費補助」這個預算項目只能給特定志工提報費用申請。

### 費用申請

這部份已開發完，但需要微調一些 UX 問題。

### 單據整合

目前單據在費用申請時**無法同時**提交給**財務組**，部分單據為電子檔可直接一併上傳，或是在籌備期間可以先拍照紀錄。

### 會計對帳

單據與費用申請項目查核，目前聽起來**財務組**在這部份也很手工。

### 結算報告

報告格式與呈現方式需要再與**財務組**確認，希望可以在格式上能調整到正確的方式輸出。

## 預計排定項目

1. 預算審核：2023 的預算建立在財務系統上完成。（2023/02）
2. 科目編碼：需與**財務組**確認單筆預算建立時附帶會計科目資訊。（2023/02）
3. 上傳單據：可上傳圖片介面、綁定費用申請項目。（2023/04）
4. 勾稽單據：單據與費用申請單查核。（2023/06）
5. 系統入帳：需確認入帳格式與資料拋轉方式。（2023/06）
6. 結算報告：需與**財務組**確認輸出格式或可在線上呈現。（2023/08）