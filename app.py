import flet as ft
import duckdb

# Simple DuckDB query to demonstrate the installed package
duckdb_result = duckdb.query("SELECT 'DuckDB로부터의 인사' AS greeting").fetchone()[0]


def main(page: ft.Page):
    page.title = "Flet Demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_button_click(e: ft.Event):
        page.snack_bar = ft.SnackBar(ft.Text("버튼이 클릭되었습니다!"))
        page.snack_bar.open = True
        page.update()

    page.add(
        ft.Text("안녕하세요, Flet 앱입니다.", size=24),
        ft.Text(duckdb_result, size=18, color="blue"),
        ft.ElevatedButton("클릭", on_click=on_button_click),
    )


if __name__ == "__main__":
    ft.app(target=main)
