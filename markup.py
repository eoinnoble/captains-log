import textwrap


font = "https://fonts.googleapis.com/css?family=Tangerine:400,700"

doc_head = textwrap.dedent(
    f"""\
    <html>
        <head>
            <title>Captain’s Log</title>
            <meta charset="UTF-8">
            <link rel='stylesheet' type='text/css' href='styles.css'>
            <link href='{font}' rel='stylesheet'>
        </head>
        <body>
    """
)

doc_end = textwrap.dedent(
    """\
    </body>
    </html>
    """
)

parchment_start = textwrap.dedent(
    """\
    <div class='parchment'>
        <div class='parchment-top'></div>
        <div class='parchment-body'>
    """
)

parchment_end = textwrap.dedent(
    """</span>
        </div>
        <div class='parchment-bottom'></div>
    </div>
    """
)
