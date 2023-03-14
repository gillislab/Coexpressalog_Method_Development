from shiny import App, render, ui
import os

species = {'maize':'Zea mays',
           'rice':'Oryza sativa',
           'arabidopsis':'Arabidopsis thaliana',
           'apple':'Malus domestica',
           'sorghum':'Sorghum bicolor',
           'grape':'Vitis vinifera',
           'mustard':'Brassica rapa',
           'soybean':'Glycine max',
           'medicago':'Medicago truncatula',
           'tobacco':'Nicotiana tabacum',
           'potato':'Solanum tuberosum',
           'brome':'Brachypodium distachyon',
           'tomato':'Solanum lycopersicum'
           }
stringent = {'moderate':'Moderate','lenient':'Lenient','stringent':'Stringent'}
#choices = {"a": "Choice A", "b": "Choice B"}
all_files_in_folder = os.listdir('/data/passala/Coexpressolog_paper_data/Species_species_gene_tables')
def ui_card(title, *args):
    return (
        ui.div(
            {"class": "card mb-4"},
            ui.div(title, class_="card-header"),
            ui.div({"class": "card-body"}, *args),
        ),
    )

app_ui = ui.page_fluid(
    ui.h1({'style':'text-align:center;'},"CPA: Coexpression Proxies for the Integration of High Dimensional Data"),
    ui.div(
        {'class':'card mb-3'},
        ui.div(
            {'class':'card-body'},
            ui.h4({"class": "card-title m-0"},'Select Species'),
            ui.div(
                {'class':'card-body overflow-auto pt-3'},
                ui.layout_sidebar(
                    ui.input_select( "species_1",'Species 1', species),
                    ui.input_select("species_2",'Species 2',species),
                ),
            ),
        ),
        ui.div(
            {'class':"card-footer"},
            ui.output_text("species_txt"),
        )
        
    ),
    ui.div(
        {'class':'card mb-3'},
        ui.div(
            {'class':'card-body'},
            ui.h4({"class": "card-title m-0"},'Select Thresholding'),
            ui.div(
                {'class':'card-body overflow-auto pt-3'},
                ui.input_select("stringency",'Coexpression Conservation Threshold', stringent),
                ),
            ),
        
        ui.div(
            {'class':"card-footer"},
            ui.output_text("stringency_txt"),
            ),
        ),
        

    ui.panel_conditional(
        "input.species_1 !== input.species_2",
        ui.div(
        {"class": "card mb-4"},
        ui.div('Download', class_="card-header"),
        ui.div(
            {"class": "card-body"},
            ui.download_button("download1","Download Coexpression Proxies")
            ),
        ),
    ),
)

#    ui.output_text_verbatim("txt"),



def server(input, output, session):
    @output
    @render.text
    def species_txt():
        if input.species_1() == input.species_2():
            return "Species are the same, please select two different species"
        else:
            return f"Generate {input.species_1()} to {input.species_2()} table"
    
    @output
    @render.text
    def stringency_txt():
            if input.species_1() == input.species_2():
                return "Awaiting species selection" 
            else:
                 return f"Generate {input.species_1()} to {input.species_2()} table with {input.stringency()} thresholding"

    @session.download(filename = lambda:f'{input.species_1()}_{input.species_2()}_{input.stringency()}_coexpressalog_table.csv')
    def download1():
        # This is the simplest case. The implementation simply returns the path to a
        # file on disk.
        spec_1_filter = [i for i in all_files_in_folder if input.species_1() in i]
        spec_2_filter = [i for i in spec_1_filter if input.species_2() in i]
        final_file = [i for i in spec_2_filter if input.stringency() in i]
        current_file = final_file[0]
        full_location = '/data/passala/Coexpressolog_paper_data/Species_species_gene_tables/'+current_file
        return full_location
app = App(app_ui, server)
