from emails.services.automated_ordering_service \
    import automated_ordering_service


def my_scheduled_job():
    automated_ordering_service()
