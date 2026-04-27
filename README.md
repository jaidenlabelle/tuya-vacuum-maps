# Tuya Vacuum Maps

🏠 View Real-Time Vacuum Maps In Home Assistant.<br>
This component adds a new camera which polls the Tuya Cloud API for the latest realtime map data.<br>
This project is primarily focused on Lefant vacuums, but aims to support all Tuya vacuums.

## Disclaimer: Supporting More Vacuums
Adding support for new vacuums is very difficult. To quote the developer of the now-discontinued `tuya_cloud_map_extractor`:

> However, compatibility with other Tuya-based vacuums is limited and often inconsistent. Adding support for new models typically requires extensive reverse engineering, decoding binary map data, and handling manufacturer-specific quirks—for each individual device or firmware version.

Since I do not have access to any of these vacuums, and since they all have different protocols and map formats without any documentation, I need you to contribute to this project with the fix for your vacuum:

- You can look through the code to see how it decodes the map format, and then download a map file from your vacuum to see what causes the error. See the [instructions for setting up a developement environment](#development-environment).
- Fix the problem for your vacuum.
- Write unit tests, and include a copy of the map and path data files for your vacuum, so that I can verify any future updates do not undo your fix.
- Create a Pull Request to merge your fixes with this repository.


## Installation

### Installing Manually

To install this integration manually, add the contents of `custom_components` to your Home Assistants `custom_components` folder and reboot.

### Installing using HACS

1. [Install HACS](https://www.hacs.xyz/docs/use/) if its not already installed.
1. Add this repository to HACS by following this guide: [HACS: Add Custom Repository](https://www.hacs.xyz/docs/faq/custom_repositories/).
3. Search for this integration using the HACS browser inside Home Assistant, and install.

## Compatibility List

This is a list of tested devices.
Create a new [issue](https://github.com/jaidenlab/tuya-vacuum-maps/issues) to add your device.

| Device                                                | Support                           |
| ----------------------------------------------------- | --------------------------------- |
| Lefant M1 | Supported |
| Lefant M2 Pro | Supported |
| Lefant N3 | Supported |
| Lebluelu SL60D | Supported |
| Lebluelu SL68 | Supported |
| Neatsvor X600 Pro | Supported |

## Development Environment

It's recommended to set up a development environment if you want to make changes to this component.

### Prerequisites

- [A Visual Studio Code + devcontainer development environment](https://developers.home-assistant.io/docs/development_environment)

### Getting Started

1. Once the devcontainer is created, fork this repository.
2. Go to the folder containing the `homeassistant-core` folder, it should be called `workspaces`.
3. Once your fork is created, make sure your terminal path is set to `/workspaces` and run `git clone <url>`.
4. To make testing easier, create a symlink to the component in your Home Assistant devcontainer.
   - Example: `ln -s /workspaces/tuya-vacuum-maps/custom_components/tuya_vacuum_maps /workspaces/homeassistant-core/config/custom_components`
5. For development, it's recommended you use a virtual environment.
   1. Create a new virtual environment (Run in the root `/tuya-vacuum-maps` folder):
      - `python -m venv venv`
   2. Activate the virtual environment:
      - `source ./venv/bin/activate`

## Special Thanks

- [Tuya Cloud Vacuum Map Extractor](https://github.com/oven-lab/tuya_cloud_map_extractor) by [@oven-lab](https://github.com/oven-lab)
