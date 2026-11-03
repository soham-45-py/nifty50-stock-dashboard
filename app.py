# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # import yfinance as yf

# # # from dash import Dash, dcc, html, dash_table
# # # from dash.dependencies import Input, Output

# # # # ============================================================
# # # # 1. NIFTY 50 COMPANY LIST + DOWNLOAD HISTORICAL DATA
# # # # ============================================================
# # # # NSE ticker symbols. These are the usual Yahoo Finance symbols;
# # # # constituents can change, so verify the official NIFTY 50 list
# # # # when updating this project.
# # # COMPANIES = {
# # #     "Adani Enterprises": "ADANIENT.NS",
# # #     "Adani Ports": "ADANIPORTS.NS",
# # #     "Apollo Hospitals": "APOLLOHOSP.NS",
# # #     "Asian Paints": "ASIANPAINT.NS",
# # #     "Axis Bank": "AXISBANK.NS",
# # #     "BSE": "BSE.NS",
# # #     "Bajaj Auto": "BAJAJ-AUTO.NS",
# # #     "Bajaj Finance": "BAJFINANCE.NS",
# # #     "Bajaj Finserv": "BAJAJFINSV.NS",
# # #     "Bharat Electronics": "BEL.NS",
# # #     "Bharti Airtel": "BHARTIARTL.NS",
# # #     "Cipla": "CIPLA.NS",
# # #     "Coal India": "COALINDIA.NS",
# # #     "Dr. Reddy's Laboratories": "DRREDDY.NS",
# # #     "Eicher Motors": "EICHERMOT.NS",
# # #     "Eternal": "ETERNAL.NS",
# # #     "Grasim Industries": "GRASIM.NS",
# # #     "HCL Technologies": "HCLTECH.NS",
# # #     "HDFC Bank": "HDFCBANK.NS",
# # #     "HDFC Life": "HDFCLIFE.NS",
# # #     "Hindalco Industries": "HINDALCO.NS",
# # #     "Hindustan Unilever": "HINDUNILVR.NS",
# # #     "ICICI Bank": "ICICIBANK.NS",
# # #     "IndiGo": "INDIGO.NS",
# # #     "Infosys": "INFY.NS",
# # #     "ITC": "ITC.NS",
# # #     "Jio Financial Services": "JIOFIN.NS",
# # #     "JSW Steel": "JSWSTEEL.NS",
# # #     "Kotak Mahindra Bank": "KOTAKBANK.NS",
# # #     "Larsen & Toubro": "LT.NS",
# # #     "Mahindra & Mahindra": "M&M.NS",
# # #     "Maruti Suzuki": "MARUTI.NS",
# # #     "Max Healthcare": "MAXHEALTH.NS",
# # #     "Nestle India": "NESTLEIND.NS",
# # #     "NTPC": "NTPC.NS",
# # #     "ONGC": "ONGC.NS",
# # #     "Power Grid Corporation": "POWERGRID.NS",
# # #     "Reliance Industries": "RELIANCE.NS",
# # #     "Shriram Finance": "SHRIRAMFIN.NS",
# # #     "SBI Life Insurance": "SBILIFE.NS",
# # #     "State Bank of India": "SBIN.NS",
# # #     "Sun Pharmaceutical": "SUNPHARMA.NS",
# # #     "Tata Consumer Products": "TATACONSUM.NS",
# # #     "Tata Motors Passenger Vehicles": "TMPV.NS",
# # #     "Tata Steel": "TATASTEEL.NS",
# # #     "TCS": "TCS.NS",
# # #     "Tech Mahindra": "TECHM.NS",
# # #     "Titan Company": "TITAN.NS",
# # #     "Trent": "TRENT.NS",
# # #     "UltraTech Cement": "ULTRACEMCO.NS",
# # # }
# # # START_DATE = "2020-01-01"
# # # END_DATE = None  # None means through the latest available date


# # # def download_company_data():
# # #     """Download daily data for the 50 tickers and combine into one table."""
# # #     ticker_list = list(COMPANIES.values())
# # #     print("Downloading historical data for NIFTY 50 companies. Please wait...")
# # #     raw = yf.download(
# # #         tickers=ticker_list,
# # #         start=START_DATE,
# # #         end=END_DATE,
# # #         group_by="ticker",
# # #         auto_adjust=False,
# # #         progress=False,
# # #         threads=True,
# # #     )

# # #     frames = []
# # #     for company, ticker in COMPANIES.items():
# # #         try:
# # #             if raw.empty:
# # #                 continue
# # #             if isinstance(raw.columns, pd.MultiIndex):
# # #                 level0 = raw.columns.get_level_values(0)
# # #                 level1 = raw.columns.get_level_values(1)
# # #                 if ticker in level0:
# # #                     one = raw[ticker].copy()
# # #                 elif ticker in level1:
# # #                     one = raw.xs(ticker, axis=1, level=1).copy()
# # #                 else:
# # #                     print(f"Skipping {company}: ticker not returned.")
# # #                     continue
# # #             else:
# # #                 one = raw.copy()

# # #             if "Close" not in one.columns:
# # #                 print(f"Skipping {company}: Close column missing.")
# # #                 continue

# # #             one = one.reset_index()
# # #             date_col = "Date" if "Date" in one.columns else one.columns[0]
# # #             one = one.rename(columns={date_col: "Date"})
# # #             one["Date"] = pd.to_datetime(one["Date"], errors="coerce")
# # #             one = one.dropna(subset=["Date", "Close"])
# # #             one["Company"] = company
# # #             one["Ticker"] = ticker
# # #             one["Daily_Return"] = pd.to_numeric(one["Close"], errors="coerce").pct_change() * 100
# # #             one["MA_20"] = pd.to_numeric(one["Close"], errors="coerce").rolling(20).mean()
# # #             one["MA_50"] = pd.to_numeric(one["Close"], errors="coerce").rolling(50).mean()
# # #             frames.append(one)

# # #         except Exception as error:
# # #             print(f"Could not process {company} ({ticker}): {error}")

# # #     if not frames:
# # #         raise RuntimeError(
# # #             "No company data was downloaded. Check internet connection, yfinance "
# # #             "installation, and whether Yahoo Finance returned data for the tickers."
# # #         )

# # #     result = pd.concat(frames, ignore_index=True)
# # #     result["Date"] = pd.to_datetime(result["Date"])
# # #     result = result.sort_values(["Company", "Date"]).reset_index(drop=True)
# # #     result.to_csv("nifty50_companies_data.csv", index=False)
# # #     print(f"Saved {result['Company'].nunique()} companies to nifty50_companies_data.csv")
# # #     print("Companies with data:", ", ".join(sorted(result["Company"].unique())))
# # #     return result


# # # df = download_company_data()

# # # # Standardize numeric columns and remove invalid rows.
# # # for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume",
# # #             "Daily_Return", "MA_20", "MA_50"]:
# # #     if col in df.columns:
# # #         df[col] = pd.to_numeric(df[col], errors="coerce")
# # # df = df.dropna(subset=["Date", "Close"]).copy()

# # # print("Combined data loaded successfully!")
# # # print("Rows:", len(df))
# # # print("Companies with data:", df["Company"].nunique())

# # # # ============================================================
# # # # 2. DASHBOARD STYLE
# # # # ============================================================
# # # app = Dash(__name__)
# # # app.title = "NIFTY 50 Individual Company Analysis"

# # # BG = "#0B1120"
# # # CARD = "#172033"
# # # TEXT = "#F1F5F9"
# # # ACCENT = "#38BDF8"
# # # BORDER = "#334155"
# # # SUBTEXT = "#94A3B8"


# # # def make_card(title, value, subtitle=""):
# # #     return html.Div(
# # #         [
# # #             html.P(title, style={"color": SUBTEXT, "fontSize": "14px", "margin": "0 0 8px"}),
# # #             html.H2(value, style={"color": ACCENT, "fontSize": "25px", "margin": "0"}),
# # #             html.P(subtitle, style={"color": SUBTEXT, "fontSize": "11px", "marginBottom": "0"}),
# # #         ],
# # #         style={"backgroundColor": CARD, "padding": "20px", "borderRadius": "12px",
# # #                "border": f"1px solid {BORDER}", "flex": "1", "minWidth": "180px"},
# # #     )


# # # def style_figure(fig):
# # #     fig.update_layout(template="plotly_dark", paper_bgcolor=CARD, plot_bgcolor=CARD,
# # #                       font_color=TEXT, margin={"l": 45, "r": 20, "t": 60, "b": 45})
# # #     return fig


# # # company_options = [{"label": name, "value": name} for name in COMPANIES if name in df["Company"].unique()]
# # # price_options = [
# # #     {"label": "Closing Price", "value": "Close"},
# # #     {"label": "Opening Price", "value": "Open"},
# # #     {"label": "Highest Price", "value": "High"},
# # #     {"label": "Lowest Price", "value": "Low"},
# # #     {"label": "Trading Volume", "value": "Volume"},
# # # ]

# # # # ============================================================
# # # # 3. DASHBOARD LAYOUT
# # # # ============================================================
# # # app.layout = html.Div(
# # #     [
# # #         html.H1("INDIAN STOCK MARKET", style={"color": ACCENT, "marginBottom": "5px"}),
# # #         html.H2("NIFTY 50 — Individual Company Trend Analysis",
# # #                 style={"marginTop": "0"}),
# # #         html.P("Explore individual NIFTY 50 companies using historical NSE stock data.",
# # #                style={"color": SUBTEXT}),
# # #         html.Hr(style={"borderColor": BORDER}),

# # #         html.Div([
# # #             html.Div([
# # #                 html.Label("Select Company", style={"fontWeight": "bold"}),
# # #                 dcc.Dropdown(id="company-filter", options=company_options,
# # #                              value=company_options[0]["value"] if company_options else None,
# # #                              clearable=False, searchable=True),
# # #             ], style={"flex": "2", "minWidth": "260px"}),
# # #             html.Div([
# # #                 html.Label("Select Date Range", style={"fontWeight": "bold"}),
# # #                 dcc.DatePickerRange(id="date-filter",
# # #                     min_date_allowed=df["Date"].min().date(),
# # #                     max_date_allowed=df["Date"].max().date(),
# # #                     start_date=df["Date"].min().date(),
# # #                     end_date=df["Date"].max().date(), display_format="DD-MM-YYYY"),
# # #             ], style={"flex": "3", "minWidth": "300px"}),
# # #         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

# # #         html.Br(),
# # #         html.Div([
# # #             html.Div([
# # #                 html.Label("Compare Companies (select multiple)", style={"fontWeight": "bold"}),
# # #                 dcc.Dropdown(id="compare-filter", options=company_options, value=[],
# # #                              multi=True, placeholder="Choose two or more companies"),
# # #             ], style={"flex": "1", "minWidth": "300px"}),
# # #             html.Div([
# # #                 html.Label("Comparison Metric"),
# # #                 dcc.Dropdown(id="compare-metric",
# # #                     options=[{"label": "Normalized Closing Price (%)", "value": "normalized"},
# # #                              {"label": "Daily Return (%)", "value": "returns"}],
# # #                     value="normalized", clearable=False),
# # #             ], style={"flex": "1", "minWidth": "250px"}),
# # #         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

# # #         html.Br(),
# # #         html.Div(id="kpi-cards", style={"display": "flex", "gap": "15px", "flexWrap": "wrap"}),
# # #         html.Br(),

# # #         html.Div([
# # #             html.Div([
# # #                 html.Label("Select Chart Type"),
# # #                 dcc.Dropdown(id="chart-type",
# # #                     options=[{"label": "Line Chart", "value": "line"},
# # #                              {"label": "Bar Chart", "value": "bar"},
# # #                              {"label": "Scatter Plot", "value": "scatter"},
# # #                              {"label": "Histogram", "value": "histogram"},
# # #                              {"label": "Box Plot", "value": "box"}],
# # #                     value="line", clearable=False),
# # #             ], style={"flex": "1", "minWidth": "220px"}),
# # #             html.Div([
# # #                 html.Label("Select Price Attribute"),
# # #                 dcc.Dropdown(id="price-attribute", options=price_options,
# # #                              value="Close", clearable=False),
# # #             ], style={"flex": "1", "minWidth": "220px"}),
# # #         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

# # #         html.Br(),
# # #         html.Div([html.H3("Individual Company Price Analysis"), dcc.Graph(id="price-chart")],
# # #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# # #         html.Br(),
# # #         html.Div([html.H3("Moving Average Analysis"), dcc.Graph(id="moving-average-chart")],
# # #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# # #         html.Br(),
# # #         html.Div([html.H3("Daily Returns Distribution"), dcc.Graph(id="returns-chart")],
# # #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# # #         html.Br(),
# # #         html.Div([html.H3("Company Comparison"), dcc.Graph(id="comparison-chart")],
# # #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# # #         html.Br(),
# # #         html.Div([
# # #             html.H3("Selected Company Data"),
# # #             dash_table.DataTable(id="data-table", page_size=10, sort_action="native",
# # #                 filter_action="native", style_table={"overflowX": "auto"},
# # #                 style_header={"backgroundColor": "#1E293B", "color": "white", "fontWeight": "bold"},
# # #                 style_cell={"backgroundColor": CARD, "color": TEXT, "padding": "10px",
# # #                             "textAlign": "left", "minWidth": "100px", "maxWidth": "220px",
# # #                             "overflow": "hidden", "textOverflow": "ellipsis"}),
# # #         ], style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# # #         html.Br(),
# # #         html.P("Project: Indian Stock Market Trend Analysis",
# # #                style={"textAlign": "center", "color": SUBTEXT}),
# # #     ],
# # #     style={"backgroundColor": BG, "color": TEXT, "minHeight": "100vh",
# # #            "padding": "25px", "fontFamily": "Arial, sans-serif"},
# # # )

# # # # ============================================================
# # # # 4. CALLBACKS
# # # # ============================================================
# # # @app.callback(
# # #     Output("kpi-cards", "children"),
# # #     Output("price-chart", "figure"),
# # #     Output("moving-average-chart", "figure"),
# # #     Output("returns-chart", "figure"),
# # #     Output("comparison-chart", "figure"),
# # #     Output("data-table", "data"),
# # #     Output("data-table", "columns"),
# # #     Input("company-filter", "value"),
# # #     Input("date-filter", "start_date"),
# # #     Input("date-filter", "end_date"),
# # #     Input("chart-type", "value"),
# # #     Input("price-attribute", "value"),
# # #     Input("compare-filter", "value"),
# # #     Input("compare-metric", "value"),
# # # )
# # # def update_dashboard(company, start_date, end_date, chart_type, attribute, compare_companies, compare_metric):
# # #     empty_fig = style_figure(go.Figure())

# # #     if not company:
# # #         empty_fig.add_annotation(text="No company data available", x=0.5, y=0.5,
# # #                                  xref="paper", yref="paper", showarrow=False)
# # #         return [make_card("No Data", "—", "Check downloaded tickers")], empty_fig, empty_fig, empty_fig, empty_fig, [], []

# # #     filtered = df[df["Company"] == company].copy()
# # #     if start_date:
# # #         filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
# # #     if end_date:
# # #         filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
# # #     filtered = filtered.sort_values("Date")

# # #     if filtered.empty:
# # #         empty_fig.add_annotation(text="No data for this company/date range", x=0.5, y=0.5,
# # #                                  xref="paper", yref="paper", showarrow=False)
# # #         return [make_card("No Data", "—", "Choose another date range")], empty_fig, empty_fig, empty_fig, empty_fig, [], []

# # #     latest_close = filtered["Close"].iloc[-1]
# # #     cards = [
# # #         make_card("Company", company, filtered["Ticker"].iloc[0]),
# # #         make_card("Latest Close", f"₹{latest_close:,.2f}", filtered["Date"].iloc[-1].strftime("%d-%m-%Y")),
# # #         make_card("Maximum Close", f"₹{filtered['Close'].max():,.2f}", "Selected period"),
# # #         make_card("Minimum Close", f"₹{filtered['Close'].min():,.2f}", "Selected period"),
# # #         make_card("Average Close", f"₹{filtered['Close'].mean():,.2f}", "Selected period"),
# # #     ]

# # #     if chart_type == "line":
# # #         price_fig = px.line(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Over Time")
# # #     elif chart_type == "bar":
# # #         price_fig = px.bar(filtered, x="Date", y=attribute, title=f"{company} — {attribute} by Date")
# # #     elif chart_type == "scatter":
# # #         price_fig = px.scatter(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Scatter Plot")
# # #     elif chart_type == "histogram":
# # #         price_fig = px.histogram(filtered, x=attribute, nbins=30, title=f"{company} — {attribute} Distribution")
# # #     elif chart_type == "box":
# # #         price_fig = px.box(filtered, y=attribute, title=f"{company} — {attribute} Box Plot")
# # #     else:
# # #         price_fig = go.Figure()
# # #     style_figure(price_fig)
# # #     price_fig.update_xaxes(title_text="Date" if chart_type not in ("histogram", "box") else "")
# # #     price_fig.update_yaxes(title_text=attribute)

# # #     ma_fig = go.Figure()
# # #     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"], mode="lines", name="Closing Price"))
# # #     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_20"], mode="lines", name="MA 20"))
# # #     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_50"], mode="lines", name="MA 50"))
# # #     ma_fig.update_layout(title=f"{company} — Closing Price vs Moving Averages",
# # #                          xaxis_title="Date", yaxis_title="Price (₹)")
# # #     style_figure(ma_fig)

# # #     returns_data = filtered.dropna(subset=["Daily_Return"])
# # #     returns_fig = px.histogram(returns_data, x="Daily_Return", nbins=30,
# # #                                title=f"{company} — Daily Return Distribution")
# # #     returns_fig.update_layout(xaxis_title="Daily Return (%)", yaxis_title="Trading Days")
# # #     style_figure(returns_fig)

# # #     # Compare companies using either normalized price (first selected date = 100)
# # #     # or daily percentage returns, so differently priced shares can be compared.
# # #     compare_fig = go.Figure()
# # #     compare_list = list(dict.fromkeys((compare_companies or []) + [company]))
# # #     compare_data = df[df["Company"].isin(compare_list)].copy()
# # #     if start_date:
# # #         compare_data = compare_data[compare_data["Date"] >= pd.to_datetime(start_date)]
# # #     if end_date:
# # #         compare_data = compare_data[compare_data["Date"] <= pd.to_datetime(end_date)]

# # #     for comp in compare_list:
# # #         one = compare_data[compare_data["Company"] == comp].sort_values("Date")
# # #         if one.empty:
# # #             continue
# # #         if compare_metric == "normalized":
# # #             first_close = one["Close"].iloc[0]
# # #             if pd.notna(first_close) and first_close != 0:
# # #                 y = (one["Close"] / first_close) * 100
# # #                 label = f"{comp} (start=100)"
# # #             else:
# # #                 continue
# # #         else:
# # #             y = one["Daily_Return"]
# # #             label = comp
# # #         compare_fig.add_trace(go.Scatter(x=one["Date"], y=y, mode="lines", name=label))
# # #     compare_fig.update_layout(
# # #         title="Company Performance Comparison" if compare_metric == "normalized" else "Daily Returns Comparison",
# # #         xaxis_title="Date",
# # #         yaxis_title="Normalized Price (start=100)" if compare_metric == "normalized" else "Daily Return (%)",
# # #     )
# # #     style_figure(compare_fig)

# # #     table_df = filtered.copy()
# # #     table_df["Date"] = table_df["Date"].dt.strftime("%Y-%m-%d")
# # #     table_df = table_df.astype(object).where(pd.notna(table_df), None)
# # #     table_data = table_df.to_dict("records")
# # #     table_columns = [{"name": col, "id": col} for col in table_df.columns]

# # #     return cards, price_fig, ma_fig, returns_fig, compare_fig, table_data, table_columns


# # # if __name__ == "__main__":
# # #     print("\nNIFTY 50 Individual Company Dashboard is starting...")
# # #     print("Open your browser at: http://127.0.0.1:8050/")
# # #     app.run(debug=False, port=8050)
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# # import yfinance as yf

# # from dash import Dash, dcc, html, dash_table
# # from dash.dependencies import Input, Output

# # # ============================================================
# # # 1. NIFTY 50 COMPANY LIST + DOWNLOAD HISTORICAL DATA
# # # ============================================================
# # # NSE ticker symbols. These are the usual Yahoo Finance symbols;
# # # constituents can change, so verify the official NIFTY 50 list
# # # when updating this project.
# # COMPANIES = {
# #     "Adani Enterprises": "ADANIENT.NS",
# #     "Adani Ports": "ADANIPORTS.NS",
# #     "Apollo Hospitals": "APOLLOHOSP.NS",
# #     "Asian Paints": "ASIANPAINT.NS",
# #     "Axis Bank": "AXISBANK.NS",
# #     "BSE": "BSE.NS",
# #     "Bajaj Auto": "BAJAJ-AUTO.NS",
# #     "Bajaj Finance": "BAJFINANCE.NS",
# #     "Bajaj Finserv": "BAJAJFINSV.NS",
# #     "Bharat Electronics": "BEL.NS",
# #     "Bharti Airtel": "BHARTIARTL.NS",
# #     "Cipla": "CIPLA.NS",
# #     "Coal India": "COALINDIA.NS",
# #     "Dr. Reddy's Laboratories": "DRREDDY.NS",
# #     "Eicher Motors": "EICHERMOT.NS",
# #     "Eternal": "ETERNAL.NS",
# #     "Grasim Industries": "GRASIM.NS",
# #     "HCL Technologies": "HCLTECH.NS",
# #     "HDFC Bank": "HDFCBANK.NS",
# #     "HDFC Life": "HDFCLIFE.NS",
# #     "Hindalco Industries": "HINDALCO.NS",
# #     "Hindustan Unilever": "HINDUNILVR.NS",
# #     "ICICI Bank": "ICICIBANK.NS",
# #     "IndiGo": "INDIGO.NS",
# #     "Infosys": "INFY.NS",
# #     "ITC": "ITC.NS",
# #     "Jio Financial Services": "JIOFIN.NS",
# #     "JSW Steel": "JSWSTEEL.NS",
# #     "Kotak Mahindra Bank": "KOTAKBANK.NS",
# #     "Larsen & Toubro": "LT.NS",
# #     "Mahindra & Mahindra": "M&M.NS",
# #     "Maruti Suzuki": "MARUTI.NS",
# #     "Max Healthcare": "MAXHEALTH.NS",
# #     "Nestle India": "NESTLEIND.NS",
# #     "NTPC": "NTPC.NS",
# #     "ONGC": "ONGC.NS",
# #     "Power Grid Corporation": "POWERGRID.NS",
# #     "Reliance Industries": "RELIANCE.NS",
# #     "Shriram Finance": "SHRIRAMFIN.NS",
# #     "SBI Life Insurance": "SBILIFE.NS",
# #     "State Bank of India": "SBIN.NS",
# #     "Sun Pharmaceutical": "SUNPHARMA.NS",
# #     "Tata Consumer Products": "TATACONSUM.NS",
# #     "Tata Motors Passenger Vehicles": "TMPV.NS",
# #     "Tata Steel": "TATASTEEL.NS",
# #     "TCS": "TCS.NS",
# #     "Tech Mahindra": "TECHM.NS",
# #     "Titan Company": "TITAN.NS",
# #     "Trent": "TRENT.NS",
# #     "UltraTech Cement": "ULTRACEMCO.NS",
# # }
# # START_DATE = "2020-01-01"
# # END_DATE = None  # None means through the latest available date


# # def download_company_data():
# #     """Download daily data for the 50 tickers and combine into one table."""
# #     ticker_list = list(COMPANIES.values())
# #     print("Downloading historical data for NIFTY 50 companies. Please wait...")
# #     raw = yf.download(
# #         tickers=ticker_list,
# #         start=START_DATE,
# #         end=END_DATE,
# #         group_by="ticker",
# #         auto_adjust=False,
# #         progress=False,
# #         threads=True,
# #     )

# #     frames = []
# #     for company, ticker in COMPANIES.items():
# #         try:
# #             if raw.empty:
# #                 continue
# #             if isinstance(raw.columns, pd.MultiIndex):
# #                 level0 = raw.columns.get_level_values(0)
# #                 level1 = raw.columns.get_level_values(1)
# #                 if ticker in level0:
# #                     one = raw[ticker].copy()
# #                 elif ticker in level1:
# #                     one = raw.xs(ticker, axis=1, level=1).copy()
# #                 else:
# #                     print(f"Skipping {company}: ticker not returned.")
# #                     continue
# #             else:
# #                 one = raw.copy()

# #             if "Close" not in one.columns:
# #                 print(f"Skipping {company}: Close column missing.")
# #                 continue

# #             one = one.reset_index()
# #             date_col = "Date" if "Date" in one.columns else one.columns[0]
# #             one = one.rename(columns={date_col: "Date"})
# #             one["Date"] = pd.to_datetime(one["Date"], errors="coerce")
# #             one = one.dropna(subset=["Date", "Close"])
# #             one["Company"] = company
# #             one["Ticker"] = ticker
# #             one["Daily_Return"] = pd.to_numeric(one["Close"], errors="coerce").pct_change() * 100
# #             one["MA_20"] = pd.to_numeric(one["Close"], errors="coerce").rolling(20).mean()
# #             one["MA_50"] = pd.to_numeric(one["Close"], errors="coerce").rolling(50).mean()
# #             frames.append(one)

# #         except Exception as error:
# #             print(f"Could not process {company} ({ticker}): {error}")

# #     if not frames:
# #         raise RuntimeError(
# #             "No company data was downloaded. Check internet connection, yfinance "
# #             "installation, and whether Yahoo Finance returned data for the tickers."
# #         )

# #     result = pd.concat(frames, ignore_index=True)
# #     result["Date"] = pd.to_datetime(result["Date"])
# #     result = result.sort_values(["Company", "Date"]).reset_index(drop=True)
# #     result.to_csv("nifty50_companies_data.csv", index=False)
# #     print(f"Saved {result['Company'].nunique()} companies to nifty50_companies_data.csv")
# #     print("Companies with data:", ", ".join(sorted(result["Company"].unique())))
# #     return result


# # df = download_company_data()

# # # Standardize numeric columns and remove invalid rows.
# # for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume",
# #             "Daily_Return", "MA_20", "MA_50"]:
# #     if col in df.columns:
# #         df[col] = pd.to_numeric(df[col], errors="coerce")
# # df = df.dropna(subset=["Date", "Close"]).copy()

# # print("Combined data loaded successfully!")
# # print("Rows:", len(df))
# # print("Companies with data:", df["Company"].nunique())

# # # ============================================================
# # # 2. DASHBOARD STYLE
# # # ============================================================
# # app = Dash(__name__)
# # app.title = "NIFTY 50 Individual Company Analysis"

# # # Fix visibility of dropdown and date-picker text on the dark dashboard.
# # app.index_string = """
# # <!DOCTYPE html>
# # <html>
# #     <head>
# #         {%metas%}
# #         <title>{%title%}</title>
# #         {%favicon%}
# #         {%css%}
# #         <style>
# #             /* Dash dropdown: readable selected value, placeholder and menu */
# #             .Select-control,
# #             .Select-menu-outer,
# #             .Select-menu,
# #             .VirtualizedSelectOption {
# #                 background-color: #ffffff !important;
# #             }
# #             .Select-value-label,
# #             .Select-placeholder,
# #             .Select-option,
# #             .VirtualizedSelectOption,
# #             .Select-input > input {
# #                 color: #1e293b !important;
# #             }
# #             .Select-option.is-focused,
# #             .VirtualizedSelectFocusedOption {
# #                 background-color: #e0f2fe !important;
# #                 color: #0f172a !important;
# #             }
# #             .Select.is-focused > .Select-control {
# #                 border-color: #38bdf8 !important;
# #                 box-shadow: 0 0 0 1px #38bdf8 !important;
# #             }

# #             /* Date range picker text and calendar */
# #             .DateRangePickerInput,
# #             .DateInput,
# #             .DateInput_input {
# #                 background-color: #ffffff !important;
# #             }
# #             .DateInput_input {
# #                 color: #1e293b !important;
# #                 font-size: 16px !important;
# #             }
# #             .DateInput_input::placeholder {
# #                 color: #64748b !important;
# #                 opacity: 1 !important;
# #             }
# #             .DateRangePickerInput_arrow_svg {
# #                 fill: #1e293b !important;
# #             }
# #             .CalendarDay__default {
# #                 color: #1e293b !important;
# #                 border-color: #e2e8f0 !important;
# #             }
# #         </style>
# #     </head>
# #     <body>
# #         {%app_entry%}
# #         <footer>
# #             {%config%}
# #             {%scripts%}
# #             {%renderer%}
# #         </footer>
# #     </body>
# # </html>
# # """

# # BG = "#0B1120"
# # CARD = "#172033"
# # TEXT = "#F1F5F9"
# # ACCENT = "#38BDF8"
# # BORDER = "#334155"
# # SUBTEXT = "#94A3B8"


# # def make_card(title, value, subtitle=""):
# #     return html.Div(
# #         [
# #             html.P(title, style={"color": SUBTEXT, "fontSize": "14px", "margin": "0 0 8px"}),
# #             html.H2(value, style={"color": ACCENT, "fontSize": "25px", "margin": "0"}),
# #             html.P(subtitle, style={"color": SUBTEXT, "fontSize": "11px", "marginBottom": "0"}),
# #         ],
# #         style={"backgroundColor": CARD, "padding": "20px", "borderRadius": "12px",
# #                "border": f"1px solid {BORDER}", "flex": "1", "minWidth": "180px"},
# #     )


# # def style_figure(fig):
# #     fig.update_layout(template="plotly_dark", paper_bgcolor=CARD, plot_bgcolor=CARD,
# #                       font_color=TEXT, margin={"l": 45, "r": 20, "t": 60, "b": 45})
# #     return fig


# # company_options = [{"label": name, "value": name} for name in COMPANIES if name in df["Company"].unique()]
# # price_options = [
# #     {"label": "Closing Price", "value": "Close"},
# #     {"label": "Opening Price", "value": "Open"},
# #     {"label": "Highest Price", "value": "High"},
# #     {"label": "Lowest Price", "value": "Low"},
# #     {"label": "Trading Volume", "value": "Volume"},
# # ]

# # # ============================================================
# # # 3. DASHBOARD LAYOUT
# # # ============================================================
# # app.layout = html.Div(
# #     [
# #         html.H1("INDIAN STOCK MARKET", style={"color": ACCENT, "marginBottom": "5px"}),
# #         html.H2("NIFTY 50 — Individual Company Trend Analysis",
# #                 style={"marginTop": "0"}),
# #         html.P("Explore individual NIFTY 50 companies using historical NSE stock data.",
# #                style={"color": SUBTEXT}),
# #         html.Hr(style={"borderColor": BORDER}),

# #         html.Div([
# #             html.Div([
# #                 html.Label("Select Company", style={"fontWeight": "bold"}),
# #                 dcc.Dropdown(id="company-filter", options=company_options,
# #                              value=company_options[0]["value"] if company_options else None,
# #                              clearable=False, searchable=True),
# #             ], style={"flex": "2", "minWidth": "260px"}),
# #             html.Div([
# #                 html.Label("Select Date Range", style={"fontWeight": "bold"}),
# #                 dcc.DatePickerRange(id="date-filter",
# #                     min_date_allowed=df["Date"].min().date(),
# #                     max_date_allowed=df["Date"].max().date(),
# #                     start_date=df["Date"].min().date(),
# #                     end_date=df["Date"].max().date(), display_format="DD-MM-YYYY"),
# #             ], style={"flex": "3", "minWidth": "300px"}),
# #         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

# #         html.Br(),
# #         html.Div([
# #             html.Div([
# #                 html.Label("Compare Companies (select multiple)", style={"fontWeight": "bold"}),
# #                 dcc.Dropdown(id="compare-filter", options=company_options, value=[],
# #                              multi=True, placeholder="Choose two or more companies"),
# #             ], style={"flex": "1", "minWidth": "300px"}),
# #             html.Div([
# #                 html.Label("Comparison Metric"),
# #                 dcc.Dropdown(id="compare-metric",
# #                     options=[{"label": "Normalized Closing Price (%)", "value": "normalized"},
# #                              {"label": "Daily Return (%)", "value": "returns"}],
# #                     value="normalized", clearable=False),
# #             ], style={"flex": "1", "minWidth": "250px"}),
# #         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

# #         html.Br(),
# #         html.Div(id="kpi-cards", style={"display": "flex", "gap": "15px", "flexWrap": "wrap"}),
# #         html.Br(),

# #         html.Div([
# #             html.Div([
# #                 html.Label("Select Chart Type"),
# #                 dcc.Dropdown(id="chart-type",
# #                     options=[{"label": "Line Chart", "value": "line"},
# #                              {"label": "Bar Chart", "value": "bar"},
# #                              {"label": "Scatter Plot", "value": "scatter"},
# #                              {"label": "Histogram", "value": "histogram"},
# #                              {"label": "Box Plot", "value": "box"}],
# #                     value="line", clearable=False),
# #             ], style={"flex": "1", "minWidth": "220px"}),
# #             html.Div([
# #                 html.Label("Select Price Attribute"),
# #                 dcc.Dropdown(id="price-attribute", options=price_options,
# #                              value="Close", clearable=False),
# #             ], style={"flex": "1", "minWidth": "220px"}),
# #         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

# #         html.Br(),
# #         html.Div([html.H3("Individual Company Price Analysis"), dcc.Graph(id="price-chart")],
# #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# #         html.Br(),
# #         html.Div([html.H3("Moving Average Analysis"), dcc.Graph(id="moving-average-chart")],
# #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# #         html.Br(),
# #         html.Div([html.H3("Daily Returns Distribution"), dcc.Graph(id="returns-chart")],
# #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# #         html.Br(),
# #         html.Div([html.H3("Company Comparison"), dcc.Graph(id="comparison-chart")],
# #                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# #         html.Br(),
# #         html.Div([
# #             html.H3("Selected Company Data"),
# #             dash_table.DataTable(id="data-table", page_size=10, sort_action="native",
# #                 filter_action="native", style_table={"overflowX": "auto"},
# #                 style_header={"backgroundColor": "#1E293B", "color": "white", "fontWeight": "bold"},
# #                 style_cell={"backgroundColor": CARD, "color": TEXT, "padding": "10px",
# #                             "textAlign": "left", "minWidth": "100px", "maxWidth": "220px",
# #                             "overflow": "hidden", "textOverflow": "ellipsis"}),
# #         ], style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
# #         html.Br(),
# #         html.P("Project: Indian Stock Market Trend Analysis",
# #                style={"textAlign": "center", "color": SUBTEXT}),
# #     ],
# #     style={"backgroundColor": BG, "color": TEXT, "minHeight": "100vh",
# #            "padding": "25px", "fontFamily": "Arial, sans-serif"},
# # )

# # # ============================================================
# # # 4. CALLBACKS
# # # ============================================================
# # @app.callback(
# #     Output("kpi-cards", "children"),
# #     Output("price-chart", "figure"),
# #     Output("moving-average-chart", "figure"),
# #     Output("returns-chart", "figure"),
# #     Output("comparison-chart", "figure"),
# #     Output("data-table", "data"),
# #     Output("data-table", "columns"),
# #     Input("company-filter", "value"),
# #     Input("date-filter", "start_date"),
# #     Input("date-filter", "end_date"),
# #     Input("chart-type", "value"),
# #     Input("price-attribute", "value"),
# #     Input("compare-filter", "value"),
# #     Input("compare-metric", "value"),
# # )
# # def update_dashboard(company, start_date, end_date, chart_type, attribute, compare_companies, compare_metric):
# #     empty_fig = style_figure(go.Figure())

# #     if not company:
# #         empty_fig.add_annotation(text="No company data available", x=0.5, y=0.5,
# #                                  xref="paper", yref="paper", showarrow=False)
# #         return [make_card("No Data", "—", "Check downloaded tickers")], empty_fig, empty_fig, empty_fig, empty_fig, [], []

# #     filtered = df[df["Company"] == company].copy()
# #     if start_date:
# #         filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
# #     if end_date:
# #         filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
# #     filtered = filtered.sort_values("Date")

# #     if filtered.empty:
# #         empty_fig.add_annotation(text="No data for this company/date range", x=0.5, y=0.5,
# #                                  xref="paper", yref="paper", showarrow=False)
# #         return [make_card("No Data", "—", "Choose another date range")], empty_fig, empty_fig, empty_fig, empty_fig, [], []

# #     latest_close = filtered["Close"].iloc[-1]
# #     cards = [
# #         make_card("Company", company, filtered["Ticker"].iloc[0]),
# #         make_card("Latest Close", f"₹{latest_close:,.2f}", filtered["Date"].iloc[-1].strftime("%d-%m-%Y")),
# #         make_card("Maximum Close", f"₹{filtered['Close'].max():,.2f}", "Selected period"),
# #         make_card("Minimum Close", f"₹{filtered['Close'].min():,.2f}", "Selected period"),
# #         make_card("Average Close", f"₹{filtered['Close'].mean():,.2f}", "Selected period"),
# #     ]

# #     if chart_type == "line":
# #         price_fig = px.line(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Over Time")
# #     elif chart_type == "bar":
# #         price_fig = px.bar(filtered, x="Date", y=attribute, title=f"{company} — {attribute} by Date")
# #     elif chart_type == "scatter":
# #         price_fig = px.scatter(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Scatter Plot")
# #     elif chart_type == "histogram":
# #         price_fig = px.histogram(filtered, x=attribute, nbins=30, title=f"{company} — {attribute} Distribution")
# #     elif chart_type == "box":
# #         price_fig = px.box(filtered, y=attribute, title=f"{company} — {attribute} Box Plot")
# #     else:
# #         price_fig = go.Figure()
# #     style_figure(price_fig)
# #     price_fig.update_xaxes(title_text="Date" if chart_type not in ("histogram", "box") else "")
# #     price_fig.update_yaxes(title_text=attribute)

# #     ma_fig = go.Figure()
# #     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"], mode="lines", name="Closing Price"))
# #     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_20"], mode="lines", name="MA 20"))
# #     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_50"], mode="lines", name="MA 50"))
# #     ma_fig.update_layout(title=f"{company} — Closing Price vs Moving Averages",
# #                          xaxis_title="Date", yaxis_title="Price (₹)")
# #     style_figure(ma_fig)

# #     returns_data = filtered.dropna(subset=["Daily_Return"])
# #     returns_fig = px.histogram(returns_data, x="Daily_Return", nbins=30,
# #                                title=f"{company} — Daily Return Distribution")
# #     returns_fig.update_layout(xaxis_title="Daily Return (%)", yaxis_title="Trading Days")
# #     style_figure(returns_fig)

# #     # Compare companies using either normalized price (first selected date = 100)
# #     # or daily percentage returns, so differently priced shares can be compared.
# #     compare_fig = go.Figure()
# #     compare_list = list(dict.fromkeys((compare_companies or []) + [company]))
# #     compare_data = df[df["Company"].isin(compare_list)].copy()
# #     if start_date:
# #         compare_data = compare_data[compare_data["Date"] >= pd.to_datetime(start_date)]
# #     if end_date:
# #         compare_data = compare_data[compare_data["Date"] <= pd.to_datetime(end_date)]

# #     for comp in compare_list:
# #         one = compare_data[compare_data["Company"] == comp].sort_values("Date")
# #         if one.empty:
# #             continue
# #         if compare_metric == "normalized":
# #             first_close = one["Close"].iloc[0]
# #             if pd.notna(first_close) and first_close != 0:
# #                 y = (one["Close"] / first_close) * 100
# #                 label = f"{comp} (start=100)"
# #             else:
# #                 continue
# #         else:
# #             y = one["Daily_Return"]
# #             label = comp
# #         compare_fig.add_trace(go.Scatter(x=one["Date"], y=y, mode="lines", name=label))
# #     compare_fig.update_layout(
# #         title="Company Performance Comparison" if compare_metric == "normalized" else "Daily Returns Comparison",
# #         xaxis_title="Date",
# #         yaxis_title="Normalized Price (start=100)" if compare_metric == "normalized" else "Daily Return (%)",
# #     )
# #     style_figure(compare_fig)

# #     table_df = filtered.copy()
# #     table_df["Date"] = table_df["Date"].dt.strftime("%Y-%m-%d")
# #     table_df = table_df.astype(object).where(pd.notna(table_df), None)
# #     table_data = table_df.to_dict("records")
# #     table_columns = [{"name": col, "id": col} for col in table_df.columns]

# #     return cards, price_fig, ma_fig, returns_fig, compare_fig, table_data, table_columns


# # if __name__ == "__main__":
# #     print("\nNIFTY 50 Individual Company Dashboard is starting...")
# #     print("Open your browser at: http://127.0.0.1:8050/")
# #     app.run(debug=False, port=8050)

# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import yfinance as yf

# from dash import Dash, dcc, html, dash_table
# from dash.dependencies import Input, Output, State

# # ============================================================
# # 1. NIFTY 50 COMPANY LIST + DOWNLOAD HISTORICAL DATA
# # ============================================================
# # NSE ticker symbols. These are the usual Yahoo Finance symbols;
# # constituents can change, so verify the official NIFTY 50 list
# # when updating this project.
# COMPANIES = {
#     "Adani Enterprises": "ADANIENT.NS",
#     "Adani Ports": "ADANIPORTS.NS",
#     "Apollo Hospitals": "APOLLOHOSP.NS",
#     "Asian Paints": "ASIANPAINT.NS",
#     "Axis Bank": "AXISBANK.NS",
#     "BSE": "BSE.NS",
#     "Bajaj Auto": "BAJAJ-AUTO.NS",
#     "Bajaj Finance": "BAJFINANCE.NS",
#     "Bajaj Finserv": "BAJAJFINSV.NS",
#     "Bharat Electronics": "BEL.NS",
#     "Bharti Airtel": "BHARTIARTL.NS",
#     "Cipla": "CIPLA.NS",
#     "Coal India": "COALINDIA.NS",
#     "Dr. Reddy's Laboratories": "DRREDDY.NS",
#     "Eicher Motors": "EICHERMOT.NS",
#     "Eternal": "ETERNAL.NS",
#     "Grasim Industries": "GRASIM.NS",
#     "HCL Technologies": "HCLTECH.NS",
#     "HDFC Bank": "HDFCBANK.NS",
#     "HDFC Life": "HDFCLIFE.NS",
#     "Hindalco Industries": "HINDALCO.NS",
#     "Hindustan Unilever": "HINDUNILVR.NS",
#     "ICICI Bank": "ICICIBANK.NS",
#     "IndiGo": "INDIGO.NS",
#     "Infosys": "INFY.NS",
#     "ITC": "ITC.NS",
#     "Jio Financial Services": "JIOFIN.NS",
#     "JSW Steel": "JSWSTEEL.NS",
#     "Kotak Mahindra Bank": "KOTAKBANK.NS",
#     "Larsen & Toubro": "LT.NS",
#     "Mahindra & Mahindra": "M&M.NS",
#     "Maruti Suzuki": "MARUTI.NS",
#     "Max Healthcare": "MAXHEALTH.NS",
#     "Nestle India": "NESTLEIND.NS",
#     "NTPC": "NTPC.NS",
#     "ONGC": "ONGC.NS",
#     "Power Grid Corporation": "POWERGRID.NS",
#     "Reliance Industries": "RELIANCE.NS",
#     "Shriram Finance": "SHRIRAMFIN.NS",
#     "SBI Life Insurance": "SBILIFE.NS",
#     "State Bank of India": "SBIN.NS",
#     "Sun Pharmaceutical": "SUNPHARMA.NS",
#     "Tata Consumer Products": "TATACONSUM.NS",
#     "Tata Motors Passenger Vehicles": "TMPV.NS",
#     "Tata Steel": "TATASTEEL.NS",
#     "TCS": "TCS.NS",
#     "Tech Mahindra": "TECHM.NS",
#     "Titan Company": "TITAN.NS",
#     "Trent": "TRENT.NS",
#     "UltraTech Cement": "ULTRACEMCO.NS",
# }
# START_DATE = "2020-01-01"
# END_DATE = None  # None means through the latest available date


# def download_company_data():
#     """Download daily data for the 50 tickers and combine into one table."""
#     ticker_list = list(COMPANIES.values())
#     print("Downloading historical data for NIFTY 50 companies. Please wait...")
#     raw = yf.download(
#         tickers=ticker_list,
#         start=START_DATE,
#         end=END_DATE,
#         group_by="ticker",
#         auto_adjust=False,
#         progress=False,
#         threads=True,
#     )

#     frames = []
#     for company, ticker in COMPANIES.items():
#         try:
#             if raw.empty:
#                 continue
#             if isinstance(raw.columns, pd.MultiIndex):
#                 level0 = raw.columns.get_level_values(0)
#                 level1 = raw.columns.get_level_values(1)
#                 if ticker in level0:
#                     one = raw[ticker].copy()
#                 elif ticker in level1:
#                     one = raw.xs(ticker, axis=1, level=1).copy()
#                 else:
#                     print(f"Skipping {company}: ticker not returned.")
#                     continue
#             else:
#                 one = raw.copy()

#             if "Close" not in one.columns:
#                 print(f"Skipping {company}: Close column missing.")
#                 continue

#             one = one.reset_index()
#             date_col = "Date" if "Date" in one.columns else one.columns[0]
#             one = one.rename(columns={date_col: "Date"})
#             one["Date"] = pd.to_datetime(one["Date"], errors="coerce")
#             one = one.dropna(subset=["Date", "Close"])
#             one["Company"] = company
#             one["Ticker"] = ticker
#             one["Daily_Return"] = pd.to_numeric(one["Close"], errors="coerce").pct_change() * 100
#             one["MA_20"] = pd.to_numeric(one["Close"], errors="coerce").rolling(20).mean()
#             one["MA_50"] = pd.to_numeric(one["Close"], errors="coerce").rolling(50).mean()
#             delta = one["Close"].diff()
#             gain = delta.clip(lower=0).rolling(14).mean()
#             loss = (-delta.clip(upper=0)).rolling(14).mean()
#             rs = gain / loss.replace(0, float("nan"))
#             one["RSI_14"] = 100 - (100 / (1 + rs))
#             rolling_std = one["Close"].rolling(20).std()
#             one["BB_Middle"] = one["Close"].rolling(20).mean()
#             one["BB_Upper"] = one["BB_Middle"] + 2 * rolling_std
#             one["BB_Lower"] = one["BB_Middle"] - 2 * rolling_std
#             frames.append(one)

#         except Exception as error:
#             print(f"Could not process {company} ({ticker}): {error}")

#     if not frames:
#         raise RuntimeError(
#             "No company data was downloaded. Check internet connection, yfinance "
#             "installation, and whether Yahoo Finance returned data for the tickers."
#         )

#     result = pd.concat(frames, ignore_index=True)
#     result["Date"] = pd.to_datetime(result["Date"])
#     result = result.sort_values(["Company", "Date"]).reset_index(drop=True)
#     result.to_csv("nifty50_companies_data.csv", index=False)
#     print(f"Saved {result['Company'].nunique()} companies to nifty50_companies_data.csv")
#     print("Companies with data:", ", ".join(sorted(result["Company"].unique())))
#     return result


# df = download_company_data()

# # Standardize numeric columns and remove invalid rows.
# for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume",
#             "Daily_Return", "MA_20", "MA_50", "RSI_14", "BB_Middle", "BB_Upper", "BB_Lower"]:
#     if col in df.columns:
#         df[col] = pd.to_numeric(df[col], errors="coerce")
# df = df.dropna(subset=["Date", "Close"]).copy()

# print("Combined data loaded successfully!")
# print("Rows:", len(df))
# print("Companies with data:", df["Company"].nunique())

# # ============================================================
# # 2. DASHBOARD STYLE
# # ============================================================
# app = Dash(__name__)
# app.title = "NIFTY 50 Individual Company Analysis"

# # Fix visibility of dropdown and date-picker text on the dark dashboard.
# app.index_string = """
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#         <style>
#             /* Dash dropdown: readable selected value, placeholder and menu */
#             .Select-control,
#             .Select-menu-outer,
#             .Select-menu,
#             .VirtualizedSelectOption {
#                 background-color: #ffffff !important;
#             }
#             .Select-value-label,
#             .Select-placeholder,
#             .Select-option,
#             .VirtualizedSelectOption,
#             .Select-input > input {
#                 color: #1e293b !important;
#             }
#             .Select-option.is-focused,
#             .VirtualizedSelectFocusedOption {
#                 background-color: #e0f2fe !important;
#                 color: #0f172a !important;
#             }
#             .Select.is-focused > .Select-control {
#                 border-color: #38bdf8 !important;
#                 box-shadow: 0 0 0 1px #38bdf8 !important;
#             }

#             /* Date range picker text and calendar */
#             .DateRangePickerInput,
#             .DateInput,
#             .DateInput_input {
#                 background-color: #ffffff !important;
#             }
#             .DateInput_input {
#                 color: #1e293b !important;
#                 font-size: 16px !important;
#             }
#             .DateInput_input::placeholder {
#                 color: #64748b !important;
#                 opacity: 1 !important;
#             }
#             .DateRangePickerInput_arrow_svg {
#                 fill: #1e293b !important;
#             }
#             .CalendarDay__default {
#                 color: #1e293b !important;
#                 border-color: #e2e8f0 !important;
#             }
#         </style>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# """

# BG = "#0B1120"
# CARD = "#172033"
# TEXT = "#F1F5F9"
# ACCENT = "#38BDF8"
# BORDER = "#334155"
# SUBTEXT = "#94A3B8"


# def make_card(title, value, subtitle=""):
#     return html.Div(
#         [
#             html.P(title, style={"color": SUBTEXT, "fontSize": "14px", "margin": "0 0 8px"}),
#             html.H2(value, style={"color": ACCENT, "fontSize": "25px", "margin": "0"}),
#             html.P(subtitle, style={"color": SUBTEXT, "fontSize": "11px", "marginBottom": "0"}),
#         ],
#         style={"backgroundColor": CARD, "padding": "20px", "borderRadius": "12px",
#                "border": f"1px solid {BORDER}", "flex": "1", "minWidth": "180px"},
#     )


# def style_figure(fig):
#     fig.update_layout(template="plotly_dark", paper_bgcolor=CARD, plot_bgcolor=CARD,
#                       font_color=TEXT, margin={"l": 45, "r": 20, "t": 60, "b": 45})
#     return fig


# company_options = [{"label": name, "value": name} for name in COMPANIES if name in df["Company"].unique()]
# price_options = [
#     {"label": "Closing Price", "value": "Close"},
#     {"label": "Opening Price", "value": "Open"},
#     {"label": "Highest Price", "value": "High"},
#     {"label": "Lowest Price", "value": "Low"},
#     {"label": "Trading Volume", "value": "Volume"},
# ]

# # ============================================================
# # 3. DASHBOARD LAYOUT
# # ============================================================
# app.layout = html.Div(
#     [
#         html.H1("INDIAN STOCK MARKET", style={"color": ACCENT, "marginBottom": "5px"}),
#         html.H2("NIFTY 50 — Individual Company Trend Analysis",
#                 style={"marginTop": "0"}),
#         html.P("Explore individual NIFTY 50 companies using historical NSE stock data.",
#                style={"color": SUBTEXT}),
#         html.Hr(style={"borderColor": BORDER}),

#         html.Div([
#             html.Div([
#                 html.Label("Select Company", style={"fontWeight": "bold"}),
#                 dcc.Dropdown(id="company-filter", options=company_options,
#                              value=company_options[0]["value"] if company_options else None,
#                              clearable=False, searchable=True),
#             ], style={"flex": "2", "minWidth": "260px"}),
#             html.Div([
#                 html.Label("Select Date Range", style={"fontWeight": "bold"}),
#                 dcc.DatePickerRange(id="date-filter",
#                     min_date_allowed=df["Date"].min().date(),
#                     max_date_allowed=df["Date"].max().date(),
#                     start_date=df["Date"].min().date(),
#                     end_date=df["Date"].max().date(), display_format="DD-MM-YYYY"),
#             ], style={"flex": "3", "minWidth": "300px"}),
#         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

#         html.Br(),
#         html.Div([
#             html.Label("Quick Date Range", style={"fontWeight": "bold"}),
#             dcc.Dropdown(
#                 id="date-preset",
#                 options=[
#                     {"label": "Full Range", "value": "all"},
#                     {"label": "1 Month", "value": "1m"},
#                     {"label": "3 Months", "value": "3m"},
#                     {"label": "6 Months", "value": "6m"},
#                     {"label": "1 Year", "value": "1y"},
#                     {"label": "5 Years", "value": "5y"},
#                 ],
#                 value="all", clearable=False, style={"maxWidth": "320px"}
#             ),
#         ]),
#         html.Br(),
#         html.Div([
#             html.Div([
#                 html.Label("Compare Companies (select multiple)", style={"fontWeight": "bold"}),
#                 dcc.Dropdown(id="compare-filter", options=company_options, value=[],
#                              multi=True, placeholder="Choose two or more companies"),
#             ], style={"flex": "1", "minWidth": "300px"}),
#             html.Div([
#                 html.Label("Comparison Metric"),
#                 dcc.Dropdown(id="compare-metric",
#                     options=[{"label": "Normalized Closing Price (%)", "value": "normalized"},
#                              {"label": "Daily Return (%)", "value": "returns"}],
#                     value="normalized", clearable=False),
#             ], style={"flex": "1", "minWidth": "250px"}),
#         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

#         html.Br(),
#         html.Div(id="kpi-cards", style={"display": "flex", "gap": "15px", "flexWrap": "wrap"}),
#         html.Br(),

#         html.Div([
#             html.Div([
#                 html.Label("Select Chart Type"),
#                 dcc.Dropdown(id="chart-type",
#                     options=[{"label": "Line Chart", "value": "line"},
#                              {"label": "Bar Chart", "value": "bar"},
#                              {"label": "Scatter Plot", "value": "scatter"},
#                              {"label": "Histogram", "value": "histogram"},
#                              {"label": "Box Plot", "value": "box"}],
#                     value="line", clearable=False),
#             ], style={"flex": "1", "minWidth": "220px"}),
#             html.Div([
#                 html.Label("Select Price Attribute"),
#                 dcc.Dropdown(id="price-attribute", options=price_options,
#                              value="Close", clearable=False),
#             ], style={"flex": "1", "minWidth": "220px"}),
#         ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

#         html.Br(),
#         html.Div([html.H3("Individual Company Price Analysis"), dcc.Graph(id="price-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([html.H3("Candlestick Chart (OHLC)"), dcc.Graph(id="candlestick-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Br(),
#         html.Div([html.H3("Moving Average Analysis"), dcc.Graph(id="moving-average-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([html.H3("Bollinger Bands Analysis"), dcc.Graph(id="bollinger-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([html.H3("RSI — Relative Strength Index"), dcc.Graph(id="rsi-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([html.H3("Daily Returns Distribution"), dcc.Graph(id="returns-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([html.H3("Company Comparison"), dcc.Graph(id="comparison-chart")],
#                  style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([
#             html.H3("Top Gainers & Losers"),
#             html.Div(id="gainers-losers"),
#         ], style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.Div([
#             html.Button("Download Filtered Data (CSV)", id="download-csv-button",
#                         n_clicks=0, style={"backgroundColor": ACCENT, "color": "#ffffff",
#                         "border": "0", "borderRadius": "8px", "padding": "11px 16px",
#                         "fontWeight": "bold", "cursor": "pointer"}),
#             dcc.Download(id="download-csv"),
#         ]),
#         html.Br(),
#         html.Div([
#             html.H3("Selected Company Data"),
#             dash_table.DataTable(id="data-table", page_size=10, sort_action="native",
#                 filter_action="native", style_table={"overflowX": "auto"},
#                 style_header={"backgroundColor": "#1E293B", "color": "white", "fontWeight": "bold"},
#                 style_cell={"backgroundColor": CARD, "color": TEXT, "padding": "10px",
#                             "textAlign": "left", "minWidth": "100px", "maxWidth": "220px",
#                             "overflow": "hidden", "textOverflow": "ellipsis"}),
#         ], style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
#         html.Br(),
#         html.P("Project: Indian Stock Market Trend Analysis",
#                style={"textAlign": "center", "color": SUBTEXT}),
#     ],
#     style={"backgroundColor": BG, "color": TEXT, "minHeight": "100vh",
#            "padding": "25px", "fontFamily": "Arial, sans-serif"},
# )

# # ============================================================
# # 4. CALLBACKS
# # ============================================================
# @app.callback(
#     Output("kpi-cards", "children"),
#     Output("price-chart", "figure"),
#     Output("candlestick-chart", "figure"),
#     Output("moving-average-chart", "figure"),
#     Output("bollinger-chart", "figure"),
#     Output("rsi-chart", "figure"),
#     Output("returns-chart", "figure"),
#     Output("comparison-chart", "figure"),
#     Output("data-table", "data"),
#     Output("data-table", "columns"),
#     Input("company-filter", "value"),
#     Input("date-filter", "start_date"),
#     Input("date-filter", "end_date"),
#     Input("chart-type", "value"),
#     Input("price-attribute", "value"),
#     Input("compare-filter", "value"),
#     Input("compare-metric", "value"),
# )
# def update_dashboard(company, start_date, end_date, chart_type, attribute, compare_companies, compare_metric):
#     empty_fig = style_figure(go.Figure())

#     if not company:
#         empty_fig.add_annotation(text="No company data available", x=0.5, y=0.5,
#                                  xref="paper", yref="paper", showarrow=False)
#         return [make_card("No Data", "—", "Check downloaded tickers")], empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, [], []

#     filtered = df[df["Company"] == company].copy()
#     if start_date:
#         filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
#     if end_date:
#         filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
#     filtered = filtered.sort_values("Date")

#     if filtered.empty:
#         empty_fig.add_annotation(text="No data for this company/date range", x=0.5, y=0.5,
#                                  xref="paper", yref="paper", showarrow=False)
#         return [make_card("No Data", "—", "Choose another date range")], empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, [], []

#     latest_close = filtered["Close"].iloc[-1]
#     cards = [
#         make_card("Company", company, filtered["Ticker"].iloc[0]),
#         make_card("Latest Close", f"₹{latest_close:,.2f}", filtered["Date"].iloc[-1].strftime("%d-%m-%Y")),
#         make_card("Maximum Close", f"₹{filtered['Close'].max():,.2f}", "Selected period"),
#         make_card("Minimum Close", f"₹{filtered['Close'].min():,.2f}", "Selected period"),
#         make_card("Average Close", f"₹{filtered['Close'].mean():,.2f}", "Selected period"),
#     ]

#     if chart_type == "line":
#         price_fig = px.line(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Over Time")
#     elif chart_type == "bar":
#         price_fig = px.bar(filtered, x="Date", y=attribute, title=f"{company} — {attribute} by Date")
#     elif chart_type == "scatter":
#         price_fig = px.scatter(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Scatter Plot")
#     elif chart_type == "histogram":
#         price_fig = px.histogram(filtered, x=attribute, nbins=30, title=f"{company} — {attribute} Distribution")
#     elif chart_type == "box":
#         price_fig = px.box(filtered, y=attribute, title=f"{company} — {attribute} Box Plot")
#     else:
#         price_fig = go.Figure()
#     style_figure(price_fig)
#     price_fig.update_xaxes(title_text="Date" if chart_type not in ("histogram", "box") else "")
#     price_fig.update_yaxes(title_text=attribute)

#     candle_fig = go.Figure(data=[go.Candlestick(
#         x=filtered["Date"], open=filtered["Open"], high=filtered["High"],
#         low=filtered["Low"], close=filtered["Close"], name="OHLC"
#     )])
#     candle_fig.update_layout(title=f"{company} — Candlestick (OHLC)",
#                              xaxis_title="Date", yaxis_title="Price (₹)",
#                              xaxis_rangeslider_visible=False)
#     style_figure(candle_fig)

#     bollinger_fig = go.Figure()
#     bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["BB_Upper"],
#                                        mode="lines", name="Upper Band"))
#     bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["BB_Lower"],
#                                        mode="lines", name="Lower Band",
#                                        fill="tonexty",
#                                        fillcolor="rgba(56,189,248,0.10)"))
#     bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["BB_Middle"],
#                                        mode="lines", name="20-Day Average"))
#     bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"],
#                                        mode="lines", name="Closing Price"))
#     bollinger_fig.update_layout(title=f"{company} — Bollinger Bands",
#                                 xaxis_title="Date", yaxis_title="Price (₹)")
#     style_figure(bollinger_fig)

#     rsi_fig = go.Figure()
#     rsi_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["RSI_14"],
#                                  mode="lines", name="RSI (14)"))
#     rsi_fig.add_hline(y=70, line_dash="dash", annotation_text="70 — Overbought")
#     rsi_fig.add_hline(y=30, line_dash="dash", annotation_text="30 — Oversold")
#     rsi_fig.update_layout(title=f"{company} — 14-Day RSI",
#                           xaxis_title="Date", yaxis_title="RSI",
#                           yaxis_range=[0, 100])
#     style_figure(rsi_fig)

#     ma_fig = go.Figure()
#     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"], mode="lines", name="Closing Price"))
#     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_20"], mode="lines", name="MA 20"))
#     ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_50"], mode="lines", name="MA 50"))
#     ma_fig.update_layout(title=f"{company} — Closing Price vs Moving Averages",
#                          xaxis_title="Date", yaxis_title="Price (₹)")
#     style_figure(ma_fig)

#     returns_data = filtered.dropna(subset=["Daily_Return"])
#     returns_fig = px.histogram(returns_data, x="Daily_Return", nbins=30,
#                                title=f"{company} — Daily Return Distribution")
#     returns_fig.update_layout(xaxis_title="Daily Return (%)", yaxis_title="Trading Days")
#     style_figure(returns_fig)

#     # Compare companies using either normalized price (first selected date = 100)
#     # or daily percentage returns, so differently priced shares can be compared.
#     compare_fig = go.Figure()
#     compare_list = list(dict.fromkeys((compare_companies or []) + [company]))
#     compare_data = df[df["Company"].isin(compare_list)].copy()
#     if start_date:
#         compare_data = compare_data[compare_data["Date"] >= pd.to_datetime(start_date)]
#     if end_date:
#         compare_data = compare_data[compare_data["Date"] <= pd.to_datetime(end_date)]

#     for comp in compare_list:
#         one = compare_data[compare_data["Company"] == comp].sort_values("Date")
#         if one.empty:
#             continue
#         if compare_metric == "normalized":
#             first_close = one["Close"].iloc[0]
#             if pd.notna(first_close) and first_close != 0:
#                 y = (one["Close"] / first_close) * 100
#                 label = f"{comp} (start=100)"
#             else:
#                 continue
#         else:
#             y = one["Daily_Return"]
#             label = comp
#         compare_fig.add_trace(go.Scatter(x=one["Date"], y=y, mode="lines", name=label))
#     compare_fig.update_layout(
#         title="Company Performance Comparison" if compare_metric == "normalized" else "Daily Returns Comparison",
#         xaxis_title="Date",
#         yaxis_title="Normalized Price (start=100)" if compare_metric == "normalized" else "Daily Return (%)",
#     )
#     style_figure(compare_fig)

#     table_df = filtered.copy()
#     table_df["Date"] = table_df["Date"].dt.strftime("%Y-%m-%d")
#     table_df = table_df.astype(object).where(pd.notna(table_df), None)
#     table_data = table_df.to_dict("records")
#     table_columns = [{"name": col, "id": col} for col in table_df.columns]

#     return cards, price_fig, candle_fig, ma_fig, bollinger_fig, rsi_fig, returns_fig, compare_fig, table_data, table_columns



# # ============================================================
# # 5. EXTRA FEATURES: DATE PRESETS, GAINERS/LOSERS, CSV EXPORT
# # ============================================================

# @app.callback(
#     Output("date-filter", "start_date"),
#     Output("date-filter", "end_date"),
#     Input("date-preset", "value"),
# )
# def apply_date_preset(preset):
#     max_date = pd.Timestamp(df["Date"].max()).normalize()
#     min_date = pd.Timestamp(df["Date"].min()).normalize()
#     offsets = {
#         "1m": pd.DateOffset(months=1),
#         "3m": pd.DateOffset(months=3),
#         "6m": pd.DateOffset(months=6),
#         "1y": pd.DateOffset(years=1),
#         "5y": pd.DateOffset(years=5),
#     }
#     if not preset or preset == "all":
#         return min_date.date(), max_date.date()
#     start = max(max_date - offsets.get(preset, pd.DateOffset(years=1)), min_date)
#     return start.date(), max_date.date()


# @app.callback(
#     Output("gainers-losers", "children"),
#     Input("date-filter", "start_date"),
#     Input("date-filter", "end_date"),
# )
# def show_gainers_losers(start_date, end_date):
#     period = df.copy()
#     if start_date:
#         period = period[period["Date"] >= pd.to_datetime(start_date)]
#     if end_date:
#         period = period[period["Date"] <= pd.to_datetime(end_date)]
#     if period.empty:
#         return html.P("No data available for this date range.")

#     summary = (period.sort_values("Date").groupby("Company")
#                .agg(first_close=("Close", "first"),
#                     latest_close=("Close", "last")).reset_index())
#     summary = summary[summary["first_close"] > 0].copy()
#     summary["Change (%)"] = (
#         (summary["latest_close"] - summary["first_close"])
#         / summary["first_close"] * 100
#     )
#     summary = summary.sort_values("Change (%)", ascending=False)

#     sections = []
#     for heading, part in [
#         ("Top 5 Gainers", summary.head(5)),
#         ("Top 5 Losers", summary.tail(5).sort_values("Change (%)")),
#     ]:
#         sections.extend([
#             html.H4(heading, style={"color": ACCENT}),
#             dash_table.DataTable(
#                 data=[{
#                     "Company": row["Company"],
#                     "Change (%)": f'{row["Change (%)"]:+.2f}%',
#                     "First Close": f'₹{row["first_close"]:,.2f}',
#                     "Latest Close": f'₹{row["latest_close"]:,.2f}',
#                 } for _, row in part.iterrows()],
#                 columns=[{"name": col, "id": col} for col in
#                          ["Company", "Change (%)", "First Close", "Latest Close"]],
#                 style_header={"backgroundColor": "#1E293B", "color": "white",
#                               "fontWeight": "bold"},
#                 style_cell={"backgroundColor": CARD, "color": TEXT,
#                             "padding": "9px", "textAlign": "left"},
#                 style_table={"overflowX": "auto"},
#             )
#         ])
#     return html.Div(sections)


# @app.callback(
#     Output("download-csv", "data"),
#     Input("download-csv-button", "n_clicks"),
#     State("company-filter", "value"),
#     State("date-filter", "start_date"),
#     State("date-filter", "end_date"),
#     prevent_initial_call=True,
# )
# def download_filtered_csv(n_clicks, company, start_date, end_date):
#     if not n_clicks or not company:
#         raise PreventUpdate
#     export_df = df[df["Company"] == company].copy()
#     if start_date:
#         export_df = export_df[export_df["Date"] >= pd.to_datetime(start_date)]
#     if end_date:
#         export_df = export_df[export_df["Date"] <= pd.to_datetime(end_date)]
#     if export_df.empty:
#         raise PreventUpdate
#     filename = company.replace(" ", "_") + "_stock_data.csv"
#     return dcc.send_data_frame(export_df.to_csv, filename, index=False)


# if __name__ == "__main__":
#     print("\nNIFTY 50 Individual Company Dashboard is starting...")
#     print("Open your browser at: http://127.0.0.1:8050/")
#     app.run(debug=False, port=8050)
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# ============================================================
# 1. NIFTY 50 COMPANY LIST + DOWNLOAD HISTORICAL DATA
# ============================================================
# NSE ticker symbols. These are the usual Yahoo Finance symbols;
# constituents can change, so verify the official NIFTY 50 list
# when updating this project.
COMPANIES = {
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Axis Bank": "AXISBANK.NS",
    "BSE": "BSE.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "Bharat Electronics": "BEL.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Cipla": "CIPLA.NS",
    "Coal India": "COALINDIA.NS",
    "Dr. Reddy's Laboratories": "DRREDDY.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Eternal": "ETERNAL.NS",
    "Grasim Industries": "GRASIM.NS",
    "HCL Technologies": "HCLTECH.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "Hindalco Industries": "HINDALCO.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "IndiGo": "INDIGO.NS",
    "Infosys": "INFY.NS",
    "ITC": "ITC.NS",
    "Jio Financial Services": "JIOFIN.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Max Healthcare": "MAXHEALTH.NS",
    "Nestle India": "NESTLEIND.NS",
    "NTPC": "NTPC.NS",
    "ONGC": "ONGC.NS",
    "Power Grid Corporation": "POWERGRID.NS",
    "Reliance Industries": "RELIANCE.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "State Bank of India": "SBIN.NS",
    "Sun Pharmaceutical": "SUNPHARMA.NS",
    "Tata Consumer Products": "TATACONSUM.NS",
    "Tata Motors Passenger Vehicles": "TMPV.NS",
    "Tata Steel": "TATASTEEL.NS",
    "TCS": "TCS.NS",
    "Tech Mahindra": "TECHM.NS",
    "Titan Company": "TITAN.NS",
    "Trent": "TRENT.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
}

# Educational sector grouping for the companies in this dashboard.
SECTORS = {
    "Adani Enterprises": "Diversified", "Adani Ports": "Infrastructure",
    "Apollo Hospitals": "Healthcare", "Asian Paints": "Consumer Goods",
    "Axis Bank": "Banking", "BSE": "Financial Services",
    "Bajaj Auto": "Automobile", "Bajaj Finance": "Financial Services",
    "Bajaj Finserv": "Financial Services", "Bharat Electronics": "Defence",
    "Bharti Airtel": "Telecom", "Cipla": "Pharmaceuticals",
    "Coal India": "Energy", "Dr. Reddy's Laboratories": "Pharmaceuticals",
    "Eicher Motors": "Automobile", "Eternal": "Consumer Services",
    "Grasim Industries": "Materials", "HCL Technologies": "Information Technology",
    "HDFC Bank": "Banking", "HDFC Life": "Insurance",
    "Hindalco Industries": "Metals", "Hindustan Unilever": "Consumer Goods",
    "ICICI Bank": "Banking", "IndiGo": "Aviation", "Infosys": "Information Technology",
    "ITC": "Consumer Goods", "Jio Financial Services": "Financial Services",
    "JSW Steel": "Metals", "Kotak Mahindra Bank": "Banking",
    "Larsen & Toubro": "Infrastructure", "Mahindra & Mahindra": "Automobile",
    "Maruti Suzuki": "Automobile", "Max Healthcare": "Healthcare",
    "Nestle India": "Consumer Goods", "NTPC": "Energy", "ONGC": "Energy",
    "Power Grid Corporation": "Utilities", "Reliance Industries": "Diversified",
    "Shriram Finance": "Financial Services", "SBI Life Insurance": "Insurance",
    "State Bank of India": "Banking", "Sun Pharmaceutical": "Pharmaceuticals",
    "Tata Consumer Products": "Consumer Goods",
    "Tata Motors Passenger Vehicles": "Automobile", "Tata Steel": "Metals",
    "TCS": "Information Technology", "Tech Mahindra": "Information Technology",
    "Titan Company": "Consumer Goods", "Trent": "Retail",
    "UltraTech Cement": "Materials",
}

START_DATE = "2020-01-01"
END_DATE = None  # None means through the latest available date


def download_company_data():
    """Download daily data for the 50 tickers and combine into one table."""
    ticker_list = list(COMPANIES.values())
    print("Downloading historical data for NIFTY 50 companies. Please wait...")
    raw = yf.download(
        tickers=ticker_list,
        start=START_DATE,
        end=END_DATE,
        group_by="ticker",
        auto_adjust=False,
        progress=False,
        threads=True,
    )

    frames = []
    for company, ticker in COMPANIES.items():
        try:
            if raw.empty:
                continue
            if isinstance(raw.columns, pd.MultiIndex):
                level0 = raw.columns.get_level_values(0)
                level1 = raw.columns.get_level_values(1)
                if ticker in level0:
                    one = raw[ticker].copy()
                elif ticker in level1:
                    one = raw.xs(ticker, axis=1, level=1).copy()
                else:
                    print(f"Skipping {company}: ticker not returned.")
                    continue
            else:
                one = raw.copy()

            if "Close" not in one.columns:
                print(f"Skipping {company}: Close column missing.")
                continue

            one = one.reset_index()
            date_col = "Date" if "Date" in one.columns else one.columns[0]
            one = one.rename(columns={date_col: "Date"})
            one["Date"] = pd.to_datetime(one["Date"], errors="coerce")
            one = one.dropna(subset=["Date", "Close"])
            one["Company"] = company
            one["Ticker"] = ticker
            one["Daily_Return"] = pd.to_numeric(one["Close"], errors="coerce").pct_change() * 100
            one["MA_20"] = pd.to_numeric(one["Close"], errors="coerce").rolling(20).mean()
            one["MA_50"] = pd.to_numeric(one["Close"], errors="coerce").rolling(50).mean()
            delta = one["Close"].diff()
            gain = delta.clip(lower=0).rolling(14).mean()
            loss = (-delta.clip(upper=0)).rolling(14).mean()
            rs = gain / loss.replace(0, float("nan"))
            one["RSI_14"] = 100 - (100 / (1 + rs))
            rolling_std = one["Close"].rolling(20).std()
            one["BB_Middle"] = one["Close"].rolling(20).mean()
            one["BB_Upper"] = one["BB_Middle"] + 2 * rolling_std
            one["BB_Lower"] = one["BB_Middle"] - 2 * rolling_std
            frames.append(one)

        except Exception as error:
            print(f"Could not process {company} ({ticker}): {error}")

    if not frames:
        raise RuntimeError(
            "No company data was downloaded. Check internet connection, yfinance "
            "installation, and whether Yahoo Finance returned data for the tickers."
        )

    result = pd.concat(frames, ignore_index=True)
    result["Date"] = pd.to_datetime(result["Date"])
    result = result.sort_values(["Company", "Date"]).reset_index(drop=True)
    result.to_csv("nifty50_companies_data.csv", index=False)
    print(f"Saved {result['Company'].nunique()} companies to nifty50_companies_data.csv")
    print("Companies with data:", ", ".join(sorted(result["Company"].unique())))
    return result

# Load saved dataset instead of downloading every time
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "nifty50_companies_data.csv")

if os.path.exists(CSV_FILE):
    print("Loading saved NIFTY 50 dataset...")
    df = pd.read_csv(CSV_FILE, parse_dates=["Date"])
    print("Saved CSV loaded successfully!")
else:
    print("Saved CSV not found. Downloading data...")
    df = download_company_data()

# Standardize numeric columns and remove invalid rows.

# Standardize numeric columns and remove invalid rows.
for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume",
            "Daily_Return", "MA_20", "MA_50", "RSI_14", "BB_Middle", "BB_Upper", "BB_Lower"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Date", "Close"]).copy()

print("Combined data loaded successfully!")
print("Rows:", len(df))
print("Companies with data:", df["Company"].nunique())

# ============================================================
# 2. DASHBOARD STYLE
# ============================================================
app = Dash(__name__)
server = app.server
app.title = "NIFTY 50 Individual Company Analysis"

# Fix visibility of dropdown and date-picker text on the dark dashboard.
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Dash dropdown: readable selected value, placeholder and menu */
            .Select-control,
            .Select-menu-outer,
            .Select-menu,
            .VirtualizedSelectOption {
                background-color: #ffffff !important;
            }
            .Select-value-label,
            .Select-placeholder,
            .Select-option,
            .VirtualizedSelectOption,
            .Select-input > input {
                color: #1e293b !important;
            }
            .Select-option.is-focused,
            .VirtualizedSelectFocusedOption {
                background-color: #e0f2fe !important;
                color: #0f172a !important;
            }
            .Select.is-focused > .Select-control {
                border-color: #38bdf8 !important;
                box-shadow: 0 0 0 1px #38bdf8 !important;
            }

            /* Date range picker text and calendar */
            .DateRangePickerInput,
            .DateInput,
            .DateInput_input {
                background-color: #ffffff !important;
            }
            .DateInput_input {
                color: #1e293b !important;
                font-size: 16px !important;
            }
            .DateInput_input::placeholder {
                color: #64748b !important;
                opacity: 1 !important;
            }
            .DateRangePickerInput_arrow_svg {
                fill: #1e293b !important;
            }
            .CalendarDay__default {
                color: #1e293b !important;
                border-color: #e2e8f0 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

BG = "#0B1120"
CARD = "#172033"
TEXT = "#F1F5F9"
ACCENT = "#38BDF8"
BORDER = "#334155"
SUBTEXT = "#94A3B8"


def make_card(title, value, subtitle=""):
    return html.Div(
        [
            html.P(title, style={"color": SUBTEXT, "fontSize": "14px", "margin": "0 0 8px"}),
            html.H2(value, style={"color": ACCENT, "fontSize": "25px", "margin": "0"}),
            html.P(subtitle, style={"color": SUBTEXT, "fontSize": "11px", "marginBottom": "0"}),
        ],
        style={"backgroundColor": CARD, "padding": "20px", "borderRadius": "12px",
               "border": f"1px solid {BORDER}", "flex": "1", "minWidth": "180px"},
    )


def style_figure(fig):
    fig.update_layout(template="plotly_dark", paper_bgcolor=CARD, plot_bgcolor=CARD,
                      font_color=TEXT, margin={"l": 45, "r": 20, "t": 60, "b": 45})
    return fig


company_options = [{"label": name, "value": name} for name in COMPANIES if name in df["Company"].unique()]
price_options = [
    {"label": "Closing Price", "value": "Close"},
    {"label": "Opening Price", "value": "Open"},
    {"label": "Highest Price", "value": "High"},
    {"label": "Lowest Price", "value": "Low"},
    {"label": "Trading Volume", "value": "Volume"},
]

# ============================================================
# 3. DASHBOARD LAYOUT
# ============================================================
app.layout = html.Div(
    [
        html.H1("INDIAN STOCK MARKET", style={"color": ACCENT, "marginBottom": "5px"}),
        html.H2("NIFTY 50 — Individual Company Trend Analysis",
                style={"marginTop": "0"}),
        html.P("Explore individual NIFTY 50 companies using historical NSE stock data.",
               style={"color": SUBTEXT}),
        html.Hr(style={"borderColor": BORDER}),

        html.Div([
            html.Div([
                html.Label("Select Company", style={"fontWeight": "bold"}),
                dcc.Dropdown(id="company-filter", options=company_options,
                             value=company_options[0]["value"] if company_options else None,
                             clearable=False, searchable=True),
            ], style={"flex": "2", "minWidth": "260px"}),
            html.Div([
                html.Label("Select Date Range", style={"fontWeight": "bold"}),
                dcc.DatePickerRange(id="date-filter",
                    min_date_allowed=df["Date"].min().date(),
                    max_date_allowed=df["Date"].max().date(),
                    start_date=df["Date"].min().date(),
                    end_date=df["Date"].max().date(), display_format="DD-MM-YYYY"),
            ], style={"flex": "3", "minWidth": "300px"}),
        ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

        html.Br(),
        html.Div([
            html.Label("Quick Date Range", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="date-preset",
                options=[
                    {"label": "Full Range", "value": "all"},
                    {"label": "1 Month", "value": "1m"},
                    {"label": "3 Months", "value": "3m"},
                    {"label": "6 Months", "value": "6m"},
                    {"label": "1 Year", "value": "1y"},
                    {"label": "5 Years", "value": "5y"},
                ],
                value="all", clearable=False, style={"maxWidth": "320px"}
            ),
        ]),
        html.Br(),
        html.Div([
            html.Div([
                html.Label("Compare Companies (select multiple)", style={"fontWeight": "bold"}),
                dcc.Dropdown(id="compare-filter", options=company_options, value=[],
                             multi=True, placeholder="Choose two or more companies"),
            ], style={"flex": "1", "minWidth": "300px"}),
            html.Div([
                html.Label("Comparison Metric"),
                dcc.Dropdown(id="compare-metric",
                    options=[{"label": "Normalized Closing Price (%)", "value": "normalized"},
                             {"label": "Daily Return (%)", "value": "returns"}],
                    value="normalized", clearable=False),
            ], style={"flex": "1", "minWidth": "250px"}),
        ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

        html.Br(),
        html.Div(id="kpi-cards", style={"display": "flex", "gap": "15px", "flexWrap": "wrap"}),
        html.Br(),

        html.Div([
            html.Div([
                html.Label("Select Chart Type"),
                dcc.Dropdown(id="chart-type",
                    options=[{"label": "Line Chart", "value": "line"},
                             {"label": "Bar Chart", "value": "bar"},
                             {"label": "Scatter Plot", "value": "scatter"},
                             {"label": "Histogram", "value": "histogram"},
                             {"label": "Box Plot", "value": "box"}],
                    value="line", clearable=False),
            ], style={"flex": "1", "minWidth": "220px"}),
            html.Div([
                html.Label("Select Price Attribute"),
                dcc.Dropdown(id="price-attribute", options=price_options,
                             value="Close", clearable=False),
            ], style={"flex": "1", "minWidth": "220px"}),
        ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),

        html.Br(),
        html.Div([html.H3("Individual Company Price Analysis"), dcc.Graph(id="price-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Candlestick Chart (OHLC)"), dcc.Graph(id="candlestick-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Br(),
        html.Div([html.H3("Moving Average Analysis"), dcc.Graph(id="moving-average-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Bollinger Bands Analysis"), dcc.Graph(id="bollinger-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("RSI — Relative Strength Index"), dcc.Graph(id="rsi-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Daily Returns Distribution"), dcc.Graph(id="returns-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Company Comparison"), dcc.Graph(id="comparison-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([
            html.H3("Top Gainers & Losers"),
            html.Div(id="gainers-losers"),
        ], style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([
            html.Button("Download Filtered Data (CSV)", id="download-csv-button",
                        n_clicks=0, style={"backgroundColor": ACCENT, "color": "#ffffff",
                        "border": "0", "borderRadius": "8px", "padding": "11px 16px",
                        "fontWeight": "bold", "cursor": "pointer"}),
            dcc.Download(id="download-csv"),
        ]),
        html.Br(),
        html.Div([
        html.Br(),
        html.Div([html.H3("Sector-wise Performance"), dcc.Graph(id="sector-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Stock Correlation Heatmap"), dcc.Graph(id="correlation-chart")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Monthly Returns Heatmap"), dcc.Graph(id="monthly-heatmap")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("52-Week High & Low"), html.Div(id="week-range-cards")],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.Div([html.H3("Volatility & Risk Analysis"), dcc.Graph(id="risk-chart"),
                  html.P("Beta is estimated against the equal-weight average return of companies in this dataset, not the official NIFTY 50 index.",
                         style={"color": SUBTEXT, "fontSize": "12px"})],
                 style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
            html.H3("Selected Company Data"),
            dash_table.DataTable(id="data-table", page_size=10, sort_action="native",
                filter_action="native", style_table={"overflowX": "auto"},
                style_header={"backgroundColor": "#1E293B", "color": "white", "fontWeight": "bold"},
                style_cell={"backgroundColor": CARD, "color": TEXT, "padding": "10px",
                            "textAlign": "left", "minWidth": "100px", "maxWidth": "220px",
                            "overflow": "hidden", "textOverflow": "ellipsis"}),
        ], style={"backgroundColor": CARD, "padding": "15px", "borderRadius": "12px"}),
        html.Br(),
        html.P("Project: Indian Stock Market Trend Analysis",
               style={"textAlign": "center", "color": SUBTEXT}),
    ],
    style={"backgroundColor": BG, "color": TEXT, "minHeight": "100vh",
           "padding": "25px", "fontFamily": "Arial, sans-serif"},
)

# ============================================================
# 4. CALLBACKS
# ============================================================
@app.callback(
    Output("kpi-cards", "children"),
    Output("price-chart", "figure"),
    Output("candlestick-chart", "figure"),
    Output("moving-average-chart", "figure"),
    Output("bollinger-chart", "figure"),
    Output("rsi-chart", "figure"),
    Output("returns-chart", "figure"),
    Output("comparison-chart", "figure"),
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Output("sector-chart", "figure"),
    Output("correlation-chart", "figure"),
    Output("monthly-heatmap", "figure"),
    Output("week-range-cards", "children"),
    Output("risk-chart", "figure"),
    Input("company-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
    Input("chart-type", "value"),
    Input("price-attribute", "value"),
    Input("compare-filter", "value"),
    Input("compare-metric", "value"),
)
def update_dashboard(company, start_date, end_date, chart_type, attribute, compare_companies, compare_metric):
    empty_fig = style_figure(go.Figure())

    if not company:
        empty_fig.add_annotation(text="No company data available", x=0.5, y=0.5,
                                 xref="paper", yref="paper", showarrow=False)
        return [make_card("No Data", "—", "Check downloaded tickers")], empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, [], [], empty_fig, empty_fig, empty_fig, [], empty_fig

    filtered = df[df["Company"] == company].copy()
    if start_date:
        filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
    filtered = filtered.sort_values("Date")

    if filtered.empty:
        empty_fig.add_annotation(text="No data for this company/date range", x=0.5, y=0.5,
                                 xref="paper", yref="paper", showarrow=False)
        return [make_card("No Data", "—", "Choose another date range")], empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, [], [], empty_fig, empty_fig, empty_fig, [], empty_fig

    latest_close = filtered["Close"].iloc[-1]
    cards = [
        make_card("Company", company, filtered["Ticker"].iloc[0]),
        make_card("Latest Close", f"₹{latest_close:,.2f}", filtered["Date"].iloc[-1].strftime("%d-%m-%Y")),
        make_card("Maximum Close", f"₹{filtered['Close'].max():,.2f}", "Selected period"),
        make_card("Minimum Close", f"₹{filtered['Close'].min():,.2f}", "Selected period"),
        make_card("Average Close", f"₹{filtered['Close'].mean():,.2f}", "Selected period"),
    ]

    if chart_type == "line":
        price_fig = px.line(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Over Time")
    elif chart_type == "bar":
        price_fig = px.bar(filtered, x="Date", y=attribute, title=f"{company} — {attribute} by Date")
    elif chart_type == "scatter":
        price_fig = px.scatter(filtered, x="Date", y=attribute, title=f"{company} — {attribute} Scatter Plot")
    elif chart_type == "histogram":
        price_fig = px.histogram(filtered, x=attribute, nbins=30, title=f"{company} — {attribute} Distribution")
    elif chart_type == "box":
        price_fig = px.box(filtered, y=attribute, title=f"{company} — {attribute} Box Plot")
    else:
        price_fig = go.Figure()
    style_figure(price_fig)
    price_fig.update_xaxes(title_text="Date" if chart_type not in ("histogram", "box") else "")
    price_fig.update_yaxes(title_text=attribute)

    candle_fig = go.Figure(data=[go.Candlestick(
        x=filtered["Date"], open=filtered["Open"], high=filtered["High"],
        low=filtered["Low"], close=filtered["Close"], name="OHLC"
    )])
    candle_fig.update_layout(title=f"{company} — Candlestick (OHLC)",
                             xaxis_title="Date", yaxis_title="Price (₹)",
                             xaxis_rangeslider_visible=False)
    style_figure(candle_fig)

    bollinger_fig = go.Figure()
    bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["BB_Upper"],
                                       mode="lines", name="Upper Band"))
    bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["BB_Lower"],
                                       mode="lines", name="Lower Band",
                                       fill="tonexty",
                                       fillcolor="rgba(56,189,248,0.10)"))
    bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["BB_Middle"],
                                       mode="lines", name="20-Day Average"))
    bollinger_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"],
                                       mode="lines", name="Closing Price"))
    bollinger_fig.update_layout(title=f"{company} — Bollinger Bands",
                                xaxis_title="Date", yaxis_title="Price (₹)")
    style_figure(bollinger_fig)

    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["RSI_14"],
                                 mode="lines", name="RSI (14)"))
    rsi_fig.add_hline(y=70, line_dash="dash", annotation_text="70 — Overbought")
    rsi_fig.add_hline(y=30, line_dash="dash", annotation_text="30 — Oversold")
    rsi_fig.update_layout(title=f"{company} — 14-Day RSI",
                          xaxis_title="Date", yaxis_title="RSI",
                          yaxis_range=[0, 100])
    style_figure(rsi_fig)

    ma_fig = go.Figure()
    ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"], mode="lines", name="Closing Price"))
    ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_20"], mode="lines", name="MA 20"))
    ma_fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["MA_50"], mode="lines", name="MA 50"))
    ma_fig.update_layout(title=f"{company} — Closing Price vs Moving Averages",
                         xaxis_title="Date", yaxis_title="Price (₹)")
    style_figure(ma_fig)

    returns_data = filtered.dropna(subset=["Daily_Return"])
    returns_fig = px.histogram(returns_data, x="Daily_Return", nbins=30,
                               title=f"{company} — Daily Return Distribution")
    returns_fig.update_layout(xaxis_title="Daily Return (%)", yaxis_title="Trading Days")
    style_figure(returns_fig)

    # Compare companies using either normalized price (first selected date = 100)
    # or daily percentage returns, so differently priced shares can be compared.
    compare_fig = go.Figure()
    compare_list = list(dict.fromkeys((compare_companies or []) + [company]))
    compare_data = df[df["Company"].isin(compare_list)].copy()
    if start_date:
        compare_data = compare_data[compare_data["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        compare_data = compare_data[compare_data["Date"] <= pd.to_datetime(end_date)]

    for comp in compare_list:
        one = compare_data[compare_data["Company"] == comp].sort_values("Date")
        if one.empty:
            continue
        if compare_metric == "normalized":
            first_close = one["Close"].iloc[0]
            if pd.notna(first_close) and first_close != 0:
                y = (one["Close"] / first_close) * 100
                label = f"{comp} (start=100)"
            else:
                continue
        else:
            y = one["Daily_Return"]
            label = comp
        compare_fig.add_trace(go.Scatter(x=one["Date"], y=y, mode="lines", name=label))
    compare_fig.update_layout(
        title="Company Performance Comparison" if compare_metric == "normalized" else "Daily Returns Comparison",
        xaxis_title="Date",
        yaxis_title="Normalized Price (start=100)" if compare_metric == "normalized" else "Daily Return (%)",
    )
    style_figure(compare_fig)

    table_df = filtered.copy()
    table_df["Date"] = table_df["Date"].dt.strftime("%Y-%m-%d")
    table_df = table_df.astype(object).where(pd.notna(table_df), None)
    table_data = table_df.to_dict("records")
    table_columns = [{"name": col, "id": col} for col in table_df.columns]


    # Sector performance: average company price change in the selected period.
    sector_source = df.copy()
    if start_date:
        sector_source = sector_source[sector_source["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        sector_source = sector_source[sector_source["Date"] <= pd.to_datetime(end_date)]
    sector_company = (sector_source.sort_values("Date").groupby("Company")
                      .agg(first=("Close", "first"), last=("Close", "last")).reset_index())
    sector_company = sector_company[sector_company["first"] > 0].copy()
    sector_company["Return (%)"] = (sector_company["last"] / sector_company["first"] - 1) * 100
    sector_company["Sector"] = sector_company["Company"].map(SECTORS).fillna("Other")
    sector_summary = sector_company.groupby("Sector", as_index=False)["Return (%)"].mean()
    sector_fig = px.bar(sector_summary.sort_values("Return (%)", ascending=False),
                        x="Sector", y="Return (%)", title="Average Company Return by Sector")
    style_figure(sector_fig)

    # Correlation matrix based on daily returns for companies with available data.
    returns_wide = sector_source.pivot_table(index="Date", columns="Company",
                                              values="Daily_Return", aggfunc="mean")
    if returns_wide.shape[1] >= 2:
        corr = returns_wide.corr()
        corr_fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.index,
                                        zmin=-1, zmax=1, colorscale="RdBu",
                                        colorbar={"title": "Correlation"}))
        corr_fig.update_layout(title="Daily Return Correlation")
    else:
        corr_fig = go.Figure()
        corr_fig.add_annotation(text="Not enough companies for correlation",
                                x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    style_figure(corr_fig)

    # Monthly return heatmap for the selected company.
    monthly_close = filtered.sort_values("Date").set_index("Date")["Close"].resample("ME").last()
    monthly_ret = monthly_close.pct_change().dropna() * 100
    if not monthly_ret.empty:
        monthly_df = monthly_ret.rename("Return").reset_index()
        monthly_df["Year"] = monthly_df["Date"].dt.year.astype(str)
        monthly_df["Month"] = monthly_df["Date"].dt.strftime("%b")
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_pivot = monthly_df.pivot(index="Year", columns="Month", values="Return").reindex(columns=month_names)
        month_fig = go.Figure(go.Heatmap(z=monthly_pivot.values, x=monthly_pivot.columns,
                                         y=monthly_pivot.index, colorscale="RdYlGn",
                                         colorbar={"title": "Return (%)"}))
        month_fig.update_layout(title=f"{company} — Monthly Returns (%)",
                                xaxis_title="Month", yaxis_title="Year")
    else:
        month_fig = go.Figure()
        month_fig.add_annotation(text="Not enough data for monthly returns",
                                  x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    style_figure(month_fig)

    # 52-week range: last 252 trading rows in the selected date window.
    last_year = filtered.tail(252)
    if not last_year.empty:
        hi, lo, latest = last_year["High"].max(), last_year["Low"].min(), last_year["Close"].iloc[-1]
        week_cards = html.Div([
            make_card("52-Week High", f"₹{hi:,.2f}", "Last 252 trading sessions"),
            make_card("52-Week Low", f"₹{lo:,.2f}", "Last 252 trading sessions"),
            make_card("Latest Close", f"₹{latest:,.2f}",
                      f"{((latest / hi - 1) * 100):+.2f}% from high | {((latest / lo - 1) * 100):+.2f}% from low"),
        ], style={"display": "flex", "gap": "15px", "flexWrap": "wrap"})
    else:
        week_cards = html.P("Not enough data for the 52-week range.")

    # Annualized volatility and estimated beta against an equal-weight dataset proxy.
    risk_data = sector_source[["Date", "Company", "Daily_Return"]].copy()
    risk_data["Daily_Return"] = pd.to_numeric(risk_data["Daily_Return"], errors="coerce")
    market_proxy = risk_data.groupby("Date")["Daily_Return"].mean().rename("Market_Proxy")
    stock_returns = risk_data[risk_data["Company"] == company].set_index("Date")["Daily_Return"]
    risk_pair = pd.concat([stock_returns.rename("Stock"), market_proxy], axis=1).dropna()
    if len(risk_pair) > 1:
        volatility = risk_pair["Stock"].std() * (252 ** 0.5)
        variance = risk_pair["Market_Proxy"].var()
        beta = risk_pair["Stock"].cov(risk_pair["Market_Proxy"]) / variance if variance else float("nan")
        risk_fig = go.Figure(go.Bar(
            x=["Annualized Volatility (%)", "Estimated Beta"],
            y=[volatility, beta],
            text=[f"{volatility:.2f}%", f"{beta:.2f}" if pd.notna(beta) else "N/A"],
            textposition="auto"
        ))
        risk_fig.update_layout(title=f"{company} — Risk Metrics",
                               yaxis_title="Metric value (different units)")
    else:
        risk_fig = go.Figure()
        risk_fig.add_annotation(text="Not enough return data for risk metrics",
                                x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    style_figure(risk_fig)

    return cards, price_fig, candle_fig, ma_fig, bollinger_fig, rsi_fig, returns_fig, compare_fig, table_data, table_columns, sector_fig, corr_fig, month_fig, week_cards, risk_fig



# ============================================================
# 5. EXTRA FEATURES: DATE PRESETS, GAINERS/LOSERS, CSV EXPORT
# ============================================================

@app.callback(
    Output("date-filter", "start_date"),
    Output("date-filter", "end_date"),
    Input("date-preset", "value"),
)
def apply_date_preset(preset):
    max_date = pd.Timestamp(df["Date"].max()).normalize()
    min_date = pd.Timestamp(df["Date"].min()).normalize()
    offsets = {
        "1m": pd.DateOffset(months=1),
        "3m": pd.DateOffset(months=3),
        "6m": pd.DateOffset(months=6),
        "1y": pd.DateOffset(years=1),
        "5y": pd.DateOffset(years=5),
    }
    if not preset or preset == "all":
        return min_date.date(), max_date.date()
    start = max(max_date - offsets.get(preset, pd.DateOffset(years=1)), min_date)
    return start.date(), max_date.date()


@app.callback(
    Output("gainers-losers", "children"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def show_gainers_losers(start_date, end_date):
    period = df.copy()
    if start_date:
        period = period[period["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        period = period[period["Date"] <= pd.to_datetime(end_date)]
    if period.empty:
        return html.P("No data available for this date range.")

    summary = (period.sort_values("Date").groupby("Company")
               .agg(first_close=("Close", "first"),
                    latest_close=("Close", "last")).reset_index())
    summary = summary[summary["first_close"] > 0].copy()
    summary["Change (%)"] = (
        (summary["latest_close"] - summary["first_close"])
        / summary["first_close"] * 100
    )
    summary = summary.sort_values("Change (%)", ascending=False)

    sections = []
    for heading, part in [
        ("Top 5 Gainers", summary.head(5)),
        ("Top 5 Losers", summary.tail(5).sort_values("Change (%)")),
    ]:
        sections.extend([
            html.H4(heading, style={"color": ACCENT}),
            dash_table.DataTable(
                data=[{
                    "Company": row["Company"],
                    "Change (%)": f'{row["Change (%)"]:+.2f}%',
                    "First Close": f'₹{row["first_close"]:,.2f}',
                    "Latest Close": f'₹{row["latest_close"]:,.2f}',
                } for _, row in part.iterrows()],
                columns=[{"name": col, "id": col} for col in
                         ["Company", "Change (%)", "First Close", "Latest Close"]],
                style_header={"backgroundColor": "#1E293B", "color": "white",
                              "fontWeight": "bold"},
                style_cell={"backgroundColor": CARD, "color": TEXT,
                            "padding": "9px", "textAlign": "left"},
                style_table={"overflowX": "auto"},
            )
        ])
    return html.Div(sections)


@app.callback(
    Output("download-csv", "data"),
    Input("download-csv-button", "n_clicks"),
    State("company-filter", "value"),
    State("date-filter", "start_date"),
    State("date-filter", "end_date"),
    prevent_initial_call=True,
)
def download_filtered_csv(n_clicks, company, start_date, end_date):
    if not n_clicks or not company:
        raise PreventUpdate
    export_df = df[df["Company"] == company].copy()
    if start_date:
        export_df = export_df[export_df["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        export_df = export_df[export_df["Date"] <= pd.to_datetime(end_date)]
    if export_df.empty:
        raise PreventUpdate
    filename = company.replace(" ", "_") + "_stock_data.csv"
    return dcc.send_data_frame(export_df.to_csv, filename, index=False)


if __name__ == "__main__":
    print("\nNIFTY 50 Individual Company Dashboard is starting...")
    print("Open your browser at: http://127.0.0.1:8050/")
    app.run(debug=False, port=8050)
