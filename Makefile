setup:
	python -m pip install -r requirements.txt
run:
	python generate_data.py && python run_pipeline.py
