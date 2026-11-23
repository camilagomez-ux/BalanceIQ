
def analyze_log(user_log):

    user_log = user_log.strip()

    if not user_log:
        return []

    results = []

    results.append(f"First character: {user_log[0]}")
    results.append(f"Last character: {user_log[-1]}")

    if "!" in user_log:
        results.append("Alert found in user log.")

    if "stress" in user_log.lower():
        results.append("NOTICE: Stress was detected in user log.")

    if "break" in user_log.lower():
        results.append("BalanceIQ suggests maintaining regular breaks.")

    if len(results) == 2:
        results.append("No specific alerts were detected.")

    return results
