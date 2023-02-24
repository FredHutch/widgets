FROM quay.io/hdc-workflows/python
LABEL author="sminot@fredhutch.org"

RUN pip3 install pandas numpy scipy statsmodels \
	pyarrow scikit-learn jinja2 plotly \
    seaborn bokeh
ADD ./ /usr/local/widgets
WORKDIR /usr/local/widgets
RUN pip3 install ./
