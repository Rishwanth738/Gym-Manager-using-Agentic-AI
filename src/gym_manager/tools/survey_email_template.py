def get_survey_email():
    """
    Returns the HTML email body for the daily gym survey.
    Replace the link with your actual Google Form URL.
    """
    gform_url = "https://forms.gle/v3H9sYgAV5pmfPGb6"

    return f"""
    <h2>Daily Gym Check-in 🏋️‍♂️</h2>
    <p>Please fill out today’s gym log:</p>
    <p><a href="{gform_url}" target="_blank">Click here to open the form</a></p>
    <br/>
    <p>Questions include:</p>
    <ul>
      <li>Did you go to the gym today? (Y/N)</li>
      <li>What muscle did you train?</li>
      <li>Did you do cardio?</li>
      <li>List exercises and sets</li>
      <li>Did you experience any pain? (Y/N)</li>
      <li>If yes, describe when and where it occurred</li>
    </ul>
    """
