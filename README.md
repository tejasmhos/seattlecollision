# Seattle Collision Research Tool

## Use Case: Duration Views

#### Name: 
set_duration

#### What it does: 
Allows user to adjust map view by setting construction window and duration range of collision data before and after construction.

#### Inputs:
 - jupyter map view of before, during, and after construction with default duration settings
 - constr_start and constr_end from jupyter interactive slider
 - collision_duration in months from jupyter interactive radio buttons (3, 6, 9, 12 months)
 - database derived from building permit and collision data that has collision counts within pre-determined radius of construction site by date, as well as start and end dates for all building construction

#### Outputs: 
Adjusted map view in jupyter notebook that represents the selected time windows.

#### Pseudo code:
 - Set constr_start and constr_end from jupyter input slider.
 - Calculate constr_dur, the duration of the construction task to be normalized.
 - Set before_start date as the constr_start minus the collision_duration selected in the jupyter radio button.
 - Set after_end date as the constr_end plus the collision_duration selected in the jupyter radio button.
 - Query all construction sites from the derived construction database that were started and completed within the (constr_start, constr_end) time frame. Set sites to display_sites.
 - Query the collision counts in the pre-defined radius for each site in display_sites in the following time frames:
   - before_ct: (before_start, constr_start)
   - during_ct: (constr_start, constr_end)
   - after_ct: (constr_end, after_end)
 - Normalize the during_ct so it reflects the same time period as before and after: 
   - during_ct_normalized = during_ct * constr_dur / collision_duration
 - Update map display:
   - Display only construction sites in display_sites.
   - Use updated before_ct, during_ct_normalized, and after_ct for map data views.
   - Allow user to re-adjust jupyter settings and repeat process with new inputs.


