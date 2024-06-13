def view_profile(youtube_service):
    """ Fetches the profile information of the authenticated user """
    request = youtube_service.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()
    return response
