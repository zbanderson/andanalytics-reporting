HTML_TEMPLATE = """
<html>
<head>
    <title>&Analytics Weekly Tear Sheet</title>
    <meta charset="utf-8" />
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

    <style>
        /* ------------------------------
           Global Layout
        ------------------------------ */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #ffffff;
            color: #222222;
        }}

        .page {{
            max-width: 900px;
            margin: 0 auto;
            padding: 36px 36px 60px 36px;
        }}

        /* ------------------------------
           Header
        ------------------------------ */
        .header {{
            border-bottom: 1px solid #cccccc;
            padding-bottom: 18px;
            margin-bottom: 28px;
        }}

        .header-title {{
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 0.02em;
        }}

        .header-sub {{
            margin-top: 6px;
            font-size: 14px;
            color: #666666;
        }}

        /* ------------------------------
           Sections
        ------------------------------ */
        .section {{
            margin-top: 32px;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin: 0 0 14px 0;
        }}

        /* ------------------------------
           Gray Strip Sections
        ------------------------------ */
        .strip {{
            background: #f2f2f2;
            padding: 18px 20px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
        }}

        /* KPI cards inside strip */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-top: 12px;
        }}

        .kpi-card {{
            background: #ffffff;
            border-radius: 6px;
            padding: 14px 16px;
            border: 1px solid #e4e4e4;
        }}

        .kpi-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #777;
        }}

        .kpi-value {{
            font-size: 20px;
            font-weight: 600;
            margin-top: 6px;
        }}

        .kpi-sub {{
            font-size: 12px;
            color: #666;
            margin-top: 2px;
        }}

        /* ------------------------------
           Charts
        ------------------------------ */
        .charts-block {{
            background: #ffffff;
            padding: 0;
            border-top: 1px solid #e0e0e0;
            border-bottom: 1px solid #e0e0e0;
        }}

        .chart {{
            margin: 32px 0;
        }}

        /* ------------------------------
           Recommendations & Insights
        ------------------------------ */
        .recs-text {{
            font-size: 14px;
            line-height: 1.7;
        }}

        .bottom-two-col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-top: 6px;
        }}

        .bullet-list {{
            font-size: 14px;
            line-height: 1.6;
            margin-left: 18px;
            padding-left: 0;
        }}

        .bullet-list li {{
            margin-bottom: 6px;
        }}
    </style>
</head>

<body>
<div class="page">

    <!-- Header -->
    <div class="header">
        <div class="header-title">&Analytics — Week of {report_period}</div>
        <div class="header-sub">Weekly tear sheet summarizing content performance, reach, engagement, and strategic insights.</div>
    </div>

    <!-- Key Metrics Section -->
    <div class="section">
        <div class="strip">
            <div class="section-title">Key Metrics</div>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Weekly Reach</div>
                    <div class="kpi-value">{weekly_reach}</div>
                    <div class="kpi-sub">{weekly_reach_change}</div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-label">Total Engagements</div>
                    <div class="kpi-value">{weekly_engagements}</div>
                    <div class="kpi-sub">ER: {weekly_engagement_rate}</div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-label">Posts This Week</div>
                    <div class="kpi-value">{num_posts}</div>
                    <div class="kpi-sub">Avg score: {avg_perf_score}</div>
                </div>
            </div>

        </div>
    </div>

    <!-- Charts Section -->
    <div class="section">
        <div class="section-title">Content Performance Charts</div>
        <div class="charts-block">
            {section_charts}
        </div>
    </div>

    <!-- Insights & Recommendations -->
    <div class="section">
        <div class="strip">
            <div class="section-title">Insights & Recommendations</div>

            <div class="bottom-two-col">

                <div>
                    <h4 style="margin:0 0 8px 0; font-size:15px;">This Week’s Highlights</h4>
                    <ul class="bullet-list">
                        {section_highlights}
                    </ul>
                </div>

                <div>
                    <h4 style="margin:0 0 8px 0; font-size:15px;">Next Week’s Focus</h4>
                    <ul class="bullet-list">
                        {section_recs}
                    </ul>
                </div>

            </div>

        </div>
    </div>

</div>
</body>
</html>
"""
