import flet as ft
import os
from colorizeUtils import colorizeImage  

def open_results_folder(e):
    results_folder = "static_images"
    if os.path.exists(results_folder):
        os.startfile(results_folder)  

def main(page: ft.Page):
    
    static_folder = "static_images"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    image_list = ft.ListView(expand=True)

    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0].path
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Selected image: {selected_file}"))
            page.snack_bar.open = True
            page.update()

            colorized_image_path = colorizeImage(selected_file)

            
            if os.path.exists(colorized_image_path):
                image_url = f"/static_images/{os.path.basename(colorized_image_path)}"
                print(f"Adding image: {image_url}")  

                image_list.controls.append(ft.Image(src=os.path.abspath(colorized_image_path), width=200, height=200))
                page.update()
            else:
                print(f"Error: file {colorized_image_path} not found!")

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    def select_and_colorize_image(e):
        file_picker.pick_files(allow_multiple=False)

    SelectImageText = ft.Container(
        content=ft.Text("Colorized images:", size=30),
        padding=ft.Padding(left=0, right=0, top=30, bottom=0)
    )

    SelectImageButton = ft.Container(
        content=ft.ElevatedButton("Select photo and colorize",
                                  on_click=select_and_colorize_image,
                                  width=300,
                                  height=55,
                                  bgcolor="#f7f7f7",
                                  color="#141414"
                                  ),
        padding=ft.Padding(left=0, right=0, top=10, bottom=0)
    )

    OpenResultsButton = ft.Container(
        content=ft.ElevatedButton("Open results folder",
                                  on_click=open_results_folder,
                                  width=220,
                                  height=55,
                                  bgcolor="#f7f7f7",
                                  color="#141414"
                                  ),
        padding=ft.Padding(left=0, right=0, top=20, bottom=20)
    )

    MainColumn = ft.Column(
        controls=[SelectImageText, SelectImageButton, image_list],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    page.add(
        ft.Column(
            controls=[
                MainColumn,
                ft.Row(
                    controls=[ft.Container(content=OpenResultsButton)],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=True
                )
            ],
            expand=True
        )
    )

ft.app(target=main, assets_dir="static_images")
