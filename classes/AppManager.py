import tkinter as tk
from tkinter import ttk, Frame, Text
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from locale import atof
import threading
import locale
from time import sleep

from classes.SeleniumHandler import SeleniumHandler
from classes.RequestHandler import RequestHandler
from classes.Database import Database

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

ENDPOINT_CONSULTA_TABELA_REFERENCIA = "/ConsultarTabelaDeReferencia"
ENDPOINT_CONSULTA_MARCAS = "/ConsultarMarcas"
ENDPOINT_CONSULTA_MODELOS = "/ConsultarModelos"
ENDPOINT_CONSULTA_ANO_MODELO = "/ConsultarAnoModelo"
ENDPOINT_CONSULTA_FIPE = "/ConsultarValorComTodosParametros"


class AppManager(tk.Tk):
    def __init__(self, request, selenium, database):
        super().__init__()
        self.request_handler = request
        self.selenium_handler = selenium
        self.connection = database
        self.build()

    def build(self):
        self.attributes("-alpha", 0.0)
        self.minsize(460, 600)
        self.center()
        self.title("Consulta de Carros e Utilitários - Byecar | Veiculos.Fipe")
        self.iconbitmap("byecar.ico")
        self.geometry("460x600")
        self.bind("<Escape>", quit)
        self.configure(padx=10, pady=10)
        self.attributes("-alpha", 0.92)

        label = ttk.Label(self, text="Consulta de Carros e Utilitários", font=("Arial", 14, "bold"))
        label.pack(padx=10, pady=10, side="top", anchor="center", expand=True)

        self.create_widgets()

    def create_widgets(self):
        tab = ttk.Notebook(self)
        tab.pack(fill="both", expand=True, anchor="center")

        self.tab_selenium = ttk.Frame(tab)
        tab.add(
            self.tab_selenium,
            text="Selenium",
            compound="top",
            padding=10,
            sticky="nsew",
        )

        self.tab_requests = ttk.Frame(tab)
        tab.add(
            self.tab_requests,
            text="Requests",
            compound="top",
            padding=10,
            sticky="nsew",
        )

        self.create_widgets_selenium()
        self.create_widgets_requests()

    def create_widgets_selenium(self):
        frame = ttk.Frame(self.tab_selenium)
        frame.pack(fill="both", expand=True, anchor="center", pady=10, padx=10, side="top")

        label = ttk.Label(
            frame,
            text="'A criatividade é a inteligência se divertindo.'\n- Albert Einstein",
            font=("Arial", 12),
            wraplength=400,
            justify="left",
        )
        label.pack(fill="both", expand=True, pady=10, side="top", anchor="n")

        checkbox = ttk.Checkbutton(
            frame,
            text="Inserir 10 registros aleatórios",
            cursor="hand2",
            style="TCheckbutton",
        )
        checkbox.state(["!alternate"])
        checkbox.pack(pady=10, side="top", anchor="center")

        text = tk.Text(frame, font=("Arial", 12), wrap="word", state="disabled")
        button = ttk.Button(
            frame,
            text="Executar",
            command=lambda: self.thread(function=insert_random_records, text=text),
            cursor="hand2",
        )
        button.pack(padx=10, side="top", anchor="center", expand=True)
        text.pack(
            fill="both",
            expand=True,
            pady=10,
            side="top",
            anchor="center",
            ipady=10,
            ipadx=10,
        )

        def insert_random_records(
            _t=text,
            _f=frame,
            _s=self.selenium_handler,
            _c=self.connection,
        ):
            if checkbox.instate(["selected"]):
                for i in range(2, 12):
                    text.config(state="normal")
                    text.insert("end", f"Registro {i-1} de 10\n")
                    self.search(
                        text=text,
                        frame=frame,
                        option=i,
                    )
            else:
                self.search(text=text, frame=frame)

    def create_widgets_requests(self):
        frame = ttk.Frame(self.tab_requests)
        frame.pack(fill="both", expand=True, anchor="center", pady=10, padx=10, side="top")

        label = ttk.Label(
            frame,
            text="'O computador surgiu para resolver problemas que antes não existiam.' - Bill Gates",
            font=("Arial", 12),
            wraplength=400,
            justify="left",
        )
        label.pack(fill="both", expand=True, pady=10, side="top", anchor="n")

        text = tk.Text(frame, font=("Arial", 12), wrap="word", state="disabled")
        self.forms(frame, text)
        text.pack(
            fill="both",
            expand=True,
            pady=10,
            side="top",
            anchor="center",
            ipady=10,
            ipadx=10,
        )

    def start(self):
        self.mainloop()

    def quit(self, event=None):
        self.selenium_handler.close_driver()
        self.connection.close()
        self.quit()

    def search(
        self,
        text: Text or None = None,
        frame: Frame or None = None,
        option: int or None = 2,
    ):
        text.config(state="normal")
        text.delete("1.0", "end")
        text.insert("end", "Executando a consulta em outra thread...\n")

        try:
            frame.children["!button"].config(state="disabled", cursor="watch", text="Consultando...")

            text.insert("end", "Iniciando o driver do Selenium...\n")
            self.selenium_handler.start_driver()

            text.insert("end", "Aguardando carregamento da página...\n")
            self.selenium_handler.get_url(url="https://veiculos.fipe.org.br/")

            # Abrir a consulta de carros e utilitários
            self.selenium_handler.find_element(
                By.CSS_SELECTOR,
                "#front > div.content > div.tab.vertical.tab-veiculos > ul > li:nth-child(1) > a",
            ).click()

            # Selecionar a tabela de referência
            try:
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectTabelaReferenciacarro_chosen").click()
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectTabelaReferenciacarro_chosen > div > ul > li:nth-child(1)").click()
            except:
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectTabelaReferenciacarro > option:nth-child(2)").click()

            try:
                # Selecionar a marca
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectMarcacarro_chosen").click()
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectMarcacarro_chosen > div > ul > li:nth-child(1)").click()
            except:
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, f"#selectMarcacarro > option:nth-child({option})").click()

            try:
                # Selecionar o modelo
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectAnoModelocarro_chosen").click()
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectAnoModelocarro_chosen > div > ul > li:nth-child(1)").click()
            except:
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectAnoModelocarro > option:nth-child(2)").click()

            # Selecionar o ano modelo
            try:
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectAnocarro_chosen").click()
                sleep(1)
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectAnocarro_chosen > div > ul > li:nth-child(2)").click()
            except:
                self.selenium_handler.find_element(By.CSS_SELECTOR, "#selectAnocarro > option:nth-child(2)").click()

            # Apertar o botão de consultar
            sleep(1)
            self.selenium_handler.find_element(By.CSS_SELECTOR, "#buttonPesquisarcarro").click()

            # Aguardar o carregamento da página
            sleep(1)
            table = self.selenium_handler.wait_for_element(By.CSS_SELECTOR, "#resultadoConsultacarroFiltros > table > tbody")

            sleep(1)

            if not table:
                raise ValueError("Tabela não encontrada")

            text.insert("end", "Resultado da consulta:\n")
            rows = table.find_elements(By.TAG_NAME, "tr")
            text.insert("end", "================================\n")
            data = {}
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                key = columns[0].text.strip(":")
                value = columns[1].text
                data[key] = value
                text.insert("end", f"{key}: {value}\n")
            text.insert("end", "================================\n")
            text.insert("end", "Consulta finalizada com sucesso\n.")
            text.insert("end", "================================\n")
            text.insert("end", "Gravando no banco de dados...\n")
            self.connection.insert(
                name=data["Modelo"],
                fipe_code=data["Código Fipe"],
                price=atof(data["Preço Médio"].replace("R$", "")),
            )
            text.insert("end", "Registro gravado com sucesso\n.")
            text.insert("end", "================================\n")
            text.insert(
                "end",
                "Observação: A consulta foi realizada selecionando os primeiros resultados das buscas dos campos de seleção. Caso deseje, no código, altere a variável 'False' para 'True' para realizar a busca digitando o valor desejado.\n",
            )
        except Exception as e:
            text.insert("end", f"Erro ao consultar: {e}")
        finally:
            frame.children["!button"].config(state="normal", cursor="hand2", text="Consultar")
            text.config(state="disabled")
            self.selenium_handler.close_driver()

    def forms(self, frame: Frame, text: Text = None):
        form = ttk.Frame(frame)
        form.pack(fill="both", expand=True, anchor="center", side="top")

        data = self.request_handler.make_request(ENDPOINT_CONSULTA_TABELA_REFERENCIA)
        if not data:
            return

        # Função para criar um combobox
        def _create_combobox(label_text, key, value, data, key_payload, callback=None):
            existing_combobox = next(
                (child for child in form.winfo_children() if child.winfo_name() == key_payload),
                None,
            )
            clicker = None
            if existing_combobox is None:
                label = tk.Label(
                    form,
                    name="l_" + key_payload,
                    text=label_text,
                    font=("Arial", 12),
                    justify="left",
                    anchor="w",
                )
                label.pack()

                combobox = ttk.Combobox(
                    form,
                    name="c_" + key_payload,
                    state="readonly",
                    justify="left",
                    style="TCombobox",
                    values=[item[key] for item in data],
                    font=("Arial", 12),
                    cursor="hand2",
                )

                clicker = lambda e: on_select(
                    key_payload=key_payload,
                    value=next(
                        (item[value] for item in data if item[key] == combobox.get()),
                        None,
                    ),
                    callback=callback,
                )
                combobox.bind("<<ComboboxSelected>>", clicker)
                combobox.pack(anchor="n", expand=True, side="top", fill="both")
            else:
                existing_combobox.bind("<<ComboboxSelected>>", clicker)

        # Combobox da Tabela de Marcas, seu evento de seleção chama a função create_model
        def create_brand():
            data = self.request_handler.make_request(ENDPOINT_CONSULTA_MARCAS)
            if not data:
                return
            _create_combobox(
                label_text="Marca",
                key="Label",
                value="Value",
                data=data,
                key_payload="codigoMarca",
                callback=create_model,
            )

        # Combobox da Tabela de Modelos, seu evento de seleção chama a função create_year_model
        def create_model():
            data = self.request_handler.make_request(ENDPOINT_CONSULTA_MODELOS)
            if not data:
                return
            _create_combobox(
                label_text="Modelo",
                key="Label",
                value="Value",
                data=data["Modelos"],
                key_payload="codigoModelo",
                callback=create_year_model,
            )

        # Combobox da Tabela de Ano Modelo, seu evento de seleção chama a função create_button
        def create_year_model():
            data = self.request_handler.make_request(ENDPOINT_CONSULTA_ANO_MODELO)
            if not data:
                return
            _create_combobox(
                label_text="Ano Modelo",
                key="Label",
                value="Value",
                data=data,
                key_payload="ano",
                callback=create_button,
            )

        # Botão de gravar a consulta no banco de dados
        def create_button():
            existing_button = next(
                (child for child in form.winfo_children() if child.winfo_name() == "submit_button"),
                None,
            )
            if existing_button is None:
                button = ttk.Button(
                    form,
                    name="submit_button",
                    text="Registrar",
                    command=lambda: self.thread(function=submit),
                    cursor="hand2",
                )
                button.pack(anchor="n", expand=True, side="top", fill="both", pady=10)

        # Função para gravar a consulta no banco de dados
        def submit(
            _: Text = None,
            frame: Frame = None,
            selenium: SeleniumHandler = None,
            database=None,
        ):
            text.config(state="normal")
            text.delete("1.0", "end")
            try:
                for child in form.winfo_children():
                    child.config(state="disabled")
                    if child.winfo_name() == "submit_button":
                        child.config(cursor="watch", text="Registrando...")

                text.insert("end", "Executando a consulta em outra thread...\n")
                data = self.request_handler.make_request(ENDPOINT_CONSULTA_FIPE)
                if not data:
                    text.insert("end", "Erro ao consultar\n")
                    return
                text.insert("end", "Consulta finalizada com sucesso\n.")
                text.insert("end", "================================\n")
                text.insert("end", "Gravando no banco de dados...\n")
                self.connection.insert(
                    name=data["Modelo"],
                    fipe_code=data["CodigoFipe"],
                    price=atof(data["Valor"].replace("R$", "")),
                )
                text.insert("end", "Registro gravado com sucesso\n.")
                text.insert("end", "================================\n")
            except Exception as e:
                text.insert("end", f"Erro ao gravar no banco de dados: {e}")
            finally:
                for child in form.winfo_children():
                    child.config(state="normal")
                    if child.winfo_name() == "submit_button":
                        child.config(cursor="arrow", text="Registrar")
                    if (child.winfo_class() == "TCombobox" or child.winfo_class() == "Label" or child.winfo_class() == "TButton") and (not child.winfo_name() == "l_codigoTabelaReferencia" and not child.winfo_name() == "c_codigoTabelaReferencia"):
                        child.destroy()
                text.config(state="disabled")

        def on_select(key_payload, value, callback=None):
            try:
                if key_payload != "ano":
                    self.request_handler.payload[key_payload] = value
                else:
                    year, fuel = value.split("-")
                    self.request_handler.payload["anoModelo"] = (int(year),)
                    self.request_handler.payload["codigoTipoCombustivel"] = (int(fuel),)
                    data = self.request_handler.make_request(ENDPOINT_CONSULTA_FIPE)
                    if text:
                        text.config(state="normal")
                        text.delete("1.0", "end")
                        text.insert("end", "================================\n")
                        text.insert("end", f"Valor: {data['Valor']}\n")
                        text.insert("end", f"Marca: {data['Marca']}\n")
                        text.insert("end", f"Modelo: {data['Modelo']}\n")
                        text.insert("end", f"Ano Modelo: {data['AnoModelo']}\n")
                        text.insert("end", f"Combustível: {data['Combustivel']}\n")
                        text.insert("end", f"Código Fipe: {data['CodigoFipe']}\n")
                        text.insert("end", f"Mês de Referência: {data['MesReferencia']}\n")
                        text.insert("end", f"Autenticação: {data['Autenticacao']}\n")
                        text.insert("end", f"Tipo de Veículo: {data['TipoVeiculo']}\n")
                        text.insert("end", f"Sigla do Combustível: {data['SiglaCombustivel']}\n")
                        text.insert("end", f"Data da Consulta: {data['DataConsulta']}\n")
                        text.insert("end", "================================\n")
                if callback:
                    callback()
            except Exception as e:
                print(e)
            finally:
                text.config(state="disabled")

        # Combobox da Tabela de Referência, seu evento de seleção chama a função create_brand
        _create_combobox(
            label_text="Tabela de Referência",
            key="Mes",
            value="Codigo",
            data=data,
            key_payload="codigoTabelaReferencia",
            callback=create_brand,
        )

    def thread(
        self,
        function,
        text: Text or None = None,
        frame: Frame or None = None,
        selenium: SeleniumHandler or None = None,
        database: Database or None = None,
    ):
        thread = threading.Thread(target=function, args=(text, frame, selenium, database))
        thread.start()

    def center(self):
        self.update_idletasks()

        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width

        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2

        self.geometry("{}x{}+{}+{}".format(width, height, x, y))

        self.deiconify()
