FROM quay.io/hdc-workflows/python
LABEL author="sminot@fredhutch.org"

RUN pip3 install pandas numpy scipy statsmodels \
	pyarrow scikit-learn jinja2 widgets-lib plotly \
    seaborn bokeh
