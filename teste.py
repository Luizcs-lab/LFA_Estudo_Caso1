import win32evtlog


def PegarLog(TipoDeLog="System", quantidade=10):
    Local = "localhost"
    coleta = win32evtlog.OpenEventLog(Local, TipoDeLog)

    pegar = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    eventos = win32evtlog.ReadEventLog(coleta, pegar, 0)

    contar = 0
    for evento in eventos:
        if contar >= quantidade:
            break
        print(
            f"[{evento.TimeGenerated}]{evento.EventType}-{evento.SourceName}-{evento.StringInserts}")
        contar += 1

        win32evtlog.CloseEventLog(coleta)


PegarLog(TipoDeLog="System", quantidade=5)
