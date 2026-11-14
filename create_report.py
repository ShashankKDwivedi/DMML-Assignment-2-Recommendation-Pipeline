from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

ROOT=Path(__file__).parent
out=ROOT/'reports/final_report.pdf'
metrics=pd.read_csv(ROOT/'reports/model_evaluation.csv')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=TA_CENTER, fontSize=18, leading=22, spaceAfter=10))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontSize=12, leading=15, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontSize=9.2, leading=13))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontSize=8, leading=10))

doc=SimpleDocTemplate(str(out), pagesize=A4, rightMargin=16*mm,leftMargin=16*mm,topMargin=14*mm,bottomMargin=14*mm)
story=[]
story += [Paragraph('End-to-End Data Management Pipeline for a Recommendation System', styles['TitleCenter']),
          Paragraph('DMML Assignment 2 — Final Report', styles['Smallx']), Spacer(1,5)]

story.append(Paragraph('1. Executive Summary', styles['H2x']))
story.append(Paragraph('This project implements a reproducible recommendation-system data pipeline covering ingestion, automated validation, time-based preparation, feature management, model training, evaluation and orchestration. A documented synthetic dataset is used so the repository can be executed without external data access. Two recommenders are compared: a popularity-based baseline and an item-based collaborative filtering model.', styles['Bodyx']))

story.append(Paragraph('2. Pipeline Design', styles['H2x']))
story.append(Image(str(ROOT/'reports/architecture.png'), width=174*mm, height=97*mm))
story.append(Spacer(1,4))
story.append(Paragraph('The workflow is dependency-ordered in run_pipeline.py. Raw CSV files are validated before preparation. The training/test split is time-based, preventing future interactions from leaking into training. Features are materialized into reusable tables, then both models are trained and evaluated with the same K=5 protocol.', styles['Bodyx']))

story.append(PageBreak())
story.append(Paragraph('3. Data Validation and Preparation', styles['H2x']))
story.append(Paragraph('The generated dataset contains 180 users, 80 items and 5,618 raw interaction rows. Four deliberately invalid interaction records are included to demonstrate automated validation: one out-of-range rating, one invalid timestamp, one unknown user ID and one unknown item ID. A duplicate row is also present and is reported by the validation stage. Invalid interaction records are separated into data/errors/invalid_interactions.csv and the validation findings are written to data/errors/validation_report.csv.', styles['Bodyx']))
story.append(Spacer(1,5))
story.append(Paragraph('After validation, 5,614 valid interactions remain. An 80/20 time-based split produces 4,491 training interactions and 1,123 test interactions. Derived datasets include user activity summaries, item popularity, a user-item interaction matrix, and reusable user/item/interaction feature tables.', styles['Bodyx']))

story.append(Paragraph('4. Feature Management', styles['H2x']))
story.append(Paragraph('The feature catalog documents reusable features including user activity count, user average rating, days since last interaction, item popularity, item average rating, popularity percentile and a positive-interaction indicator. Features are stored separately from raw and processed data so the same definitions can be reused during training and prediction.', styles['Bodyx']))

story.append(Paragraph('5. Model Training and Evaluation', styles['H2x']))
data=[['Model','Precision@5','Recall@5','NDCG@5','Coverage','Diversity']]
for _,r in metrics.iterrows():
    data.append([r['Model'],f"{r['Precision@K']:.4f}",f"{r['Recall@K']:.4f}",f"{r['NDCG@K']:.4f}",f"{r['Coverage']:.4f}",f"{r['Diversity']:.4f}"])
t=Table(data,colWidths=[58*mm,25*mm,25*mm,25*mm,25*mm,25*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.5,colors.grey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7.5),('ALIGN',(1,1),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.whitesmoke])]))
story.append(t)
story.append(Spacer(1,5))
story.append(Paragraph('The popularity baseline provides slightly stronger precision, recall and NDCG on this synthetic temporal test set, while item-based collaborative filtering provides substantially higher catalog coverage and higher category diversity. This demonstrates the intended trade-off between a simple global recommender and a personalized recommender.', styles['Bodyx']))

story.append(PageBreak())
story.append(Paragraph('6. Experiment Tracking and Orchestration', styles['H2x']))
story.append(Paragraph('Each model run records the model name, timestamp, K value, split strategy, evaluation metrics and model artifact path in artifacts/experiment_runs.json. The structured Python workflow provides explicit task dependencies and can be scheduled using an operating-system scheduler. The repository also includes dags/recommendation_pipeline.py as a scheduler entry point.', styles['Bodyx']))
story.append(Spacer(1,4))
story.append(Paragraph('7. Successful Execution Evidence', styles['H2x']))
story.append(Image(str(ROOT/'reports/pipeline_success_capture.png'), width=174*mm, height=73*mm))
story.append(Spacer(1,4))
story.append(Paragraph('The execution capture above corresponds to the repository pipeline run used to validate the delivered artifacts. It ends with “PIPELINE STATUS: SUCCESS”.', styles['Smallx']))

story.append(Paragraph('8. Limitations and Improvements', styles['H2x']))
story.append(Paragraph('The project uses synthetic interactions and therefore does not represent real-world user behavior. The item-CF model is intentionally simple and does not include implicit-feedback weighting, cold-start features or online serving. A production extension would use a public dataset such as MovieLens, add a hybrid content/collaborative model, introduce feature-store or database persistence, and use MLflow or another managed experiment-tracking service. Evaluation could also add confidence intervals and repeated temporal backtests.', styles['Bodyx']))

story.append(Paragraph('9. Conclusion', styles['H2x']))
story.append(Paragraph('The delivered repository satisfies the requested end-to-end structure and emphasizes clean modular components, reproducibility, validation, reusable features, comparable model evaluation and explicit orchestration rather than only model accuracy.', styles['Bodyx']))

doc.build(story)
print(out)
