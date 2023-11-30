def input_ticker():
    # Initialize an empty list to store ticker symbols
    tickers = []

    while True:
        # Ask the user for input
        ticker = input("Enter a 3-letter ticker symbol (or 'q' to quit): ").strip().upper()

        # Check if the input is 'q' to quit the loop
        if ticker == 'Q':
            break

        # Check if the input is a valid 3-letter ticker symbol
        if len(ticker) == 3:
            tickers.append(ticker)
            print(f'Ticker "{ticker}" added to the list.')
        else:
            print('Invalid ticker symbol. Please enter a valid 3-letter symbol.')

    # Display the collected ticker symbols
    if tickers:
        print('Collected ticker symbols:')
        for ticker in tickers:
            print(ticker)
    else:
        print('No ticker symbols collected.')

    return tickers