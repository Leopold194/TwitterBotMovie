def cutSummaryIn2(summary):
    limit = 255
    while summary[limit] != " " and summary[limit] != "." and summary[limit] != ",":
        limit -= 1
    return [summary[:limit+1], summary[limit+1:]]

def cutSummaryIn3(summary):
    summaryParts = []
    for _ in range(2):
        limit = 255
        while summary[limit] != " " and summary[limit] != "." and summary[limit] != ",":
            limit -= 1
        summaryParts.append(summary[:limit+1])
        summary = summary[limit+1:]
    summaryParts.append(summary)
    return summaryParts

def getMovieOfDay():
    
    import json

    with open('utils/data/BDD.json', 'r') as f:
        try:
            data = json.load(f)
            rank_to_today = list(data.keys())[-1]
        except json.decoder.JSONDecodeError:
            rank_to_today = 250
    
    return rank_to_today