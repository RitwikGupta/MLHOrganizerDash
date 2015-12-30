### MLH Organizer Dash 💻

This is a WIP, allowing hackathons that use [MyMLH](https://my.mlh.io) to see their registrations in any easy to use interface.  

## Screenshots  


<table>
  <tr>
    <td align="center">
      <a href="http:/https://raw.githubusercontent.com/RitwikGupta/MLHOrganizerDash/master/scrn/registrations.PNG" target="_blank" title="Registrants">
        <img src="https://raw.githubusercontent.com/RitwikGupta/MLHOrganizerDash/master/scrn/registrations.PNG" alt="Apps">
      </a>
      <br />
      <em>Registrants</em>
    </td>
    <td align="center">
      <a href="https://raw.githubusercontent.com/RitwikGupta/MLHOrganizerDash/master/scrn/stats.PNG" target="_blank" title="Stats">
        <img src="https://raw.githubusercontent.com/RitwikGupta/MLHOrganizerDash/master/scrn/stats.PNG" alt="Stats">
      </a>
      <br />
      <em>Stats</em>
    </td>
  </tr>
</table>

## Requirements  
1. Python 2.7.6+  
1. virtualenv (`pip install virtualenv`)  
1. Flask  
  
(You can install Flask by running `pip install -r requirements.txt`)  

## How to use  

1. Clone this repository and `cd` to it  
1. Create a virtual environment called `venv` by `virtualenv venv`  
1. Activate the virtualenv by `. venv/bin/activate`  
1. Install all requirements inside the virtualenv by `pip install -r requirements.txt`  
1. Edit `dash/config.py` to your needs  
1. Run the server via `python dash/views.py`
