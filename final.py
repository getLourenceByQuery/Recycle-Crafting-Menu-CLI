from rich.console import Console
from rich.columns import Columns
from rich.console import Group
from rich.prompt import Prompt
from rich.align import Align
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from getpass import getpass
from rich import box
import re
import os
import json

console = Console()



## #info-------------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------PANG CONVERT NG JSON CONTENT INTO DICT-----------------------------------------------------------------



def converter(data):

    if isinstance(data, dict):
        
        tempDictionary = {}
        for key, value in data.items():
            
            if isinstance(key, str) and key.isdigit():
                tempkey = int(key)
            else:
                tempkey = key
            tempDictionary[tempkey] = converter(value)
            
        return tempDictionary
    
    elif isinstance(data, list):
        return [converter(item) for item in data]
    
    else:
        return data
    
base_dir = os.path.dirname(os.path.abspath(__file__))
jsonPath = os.path.join(base_dir, 'products.json')
with open(jsonPath, 'r') as f:
    rawProducts = json.load(f)
    
products = converter(rawProducts)




## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------PANG CLEAR NG SCREEN--------------------------------------------------------------------------



def clearScreen():
    if os.name == 'nt' :
        os.system('cls')
    else:
        os.system('clear')



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------FOR DISPLAYING THE HEADER-----------------------------------------------------------------



def displayHeader():

    headerTitle = """
.--------------------------------------------------------------------------------------------------------------------------------------.
|                                                                                                                                      |
|  ░█▀▄░█▀▀░█▀▀░█░█░█▀▀░█░░░█▀▀░░░█▀▀░█▀▄░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀▀░░░▀█▀░█▀█░█▀▀░▀█▀░█▀▄░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀░░░█▄█░█▀▀░█▀█░█░█  |
|  ░█▀▄░█▀▀░█░░░░█░░█░░░█░░░█▀▀░░░█░░░█▀▄░█▀█░█▀▀░░█░░░█░░█░█░█░█░░░░█░░█░█░▀▀█░░█░░█▀▄░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█░░░█░█░█▀▀░█░█░█░█  |
|  ░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀░░░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀  |
|                                                                                                                                      |
'--------------------------------------------------------------------------------------------------------------------------------------'
"""
    centerHeader = Align.center(headerTitle)

    panelHeader = Panel(
        centerHeader,
        border_style="#4cbfc7 underline on #001515",
        box=box.ROUNDED,
        style= "#00BCBC")

    console.print(panelHeader)




## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------PARA SA PAGCHECK NG CHOICES-----------------------------------------------------------------


def choiceChecker(prompt_text: str):
    while True:
        try:
            choiceMenus = Prompt.ask(prompt_text )
            choiceMenu = int(choiceMenus)
            return choiceMenu, None 

        except ValueError:
            errorMessage = "[bold red]INVALID INPUT! ENTER A NUMBER ONLY[/bold red]"
            return None, errorMessage



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------FOR DISPLAYING THE INSTRUCTIONS-----------------------------------------------------------------



def instructions(productIndex, material, searchResult, errorMessage=None):

    def choiceBack(choice):
        if choice == 0:
            return 0
        else:
            return choice
    
    clearScreen()
    if errorMessage:
        panelError = Panel(
            errorMessage,
            border_style="red",
            box=box.ROUNDED,
            padding=(0, 2)
        )
        console.print(panelError)
    displayHeader()
    console.print(Rule(style="#4cbfc7", characters="_"))
    print("\n")

    productData = None
    titleText = ""
    
    # #warning ------------------------------------------------------------------------------------------------------------------------------------------------
    # #warning ----------------------------------------------PARA SA SEARCH-------------------------------------------------------
    
    if material == 0:
        
        for m in products:
            for i in products[m]:
                if products[m][i]['title'] == searchResult:
                    productData = products[m][i]
                    productMaterials = products[m][i]['materials']
                    productTools = products[m][i]['tools']
                    titleText = products[m][i]['title']
                    break
            if productData:
                break
            
    # #warning ------------------------------------------------------------------------------------------------------------------------------------------------
    # #warning ----------------------------------------------PARA SA MATERIAL SELECTION-------------------------------------------------------
    
    else: 
        productData = products[material][productIndex]
        productMaterials = products[material][productIndex]['materials']
        productTools = products[material][productIndex]['tools']
        titleText = products[material][productIndex]['title']




    
    stepContent = f"[bold #4cbfc7]MATERIALS NEEDED:[/bold #4cbfc7] {', '.join(productMaterials).upper()}\n[bold #4cbfc7]TOOLS NEEDED:[/bold #4cbfc7] {', '.join(productTools).upper()}\n\n" 
    for idx, step in enumerate(productData["steps"]):
        stepContent += f"[bold #4cbfc7][STEP {idx+1}][/bold #4cbfc7] {step}\n\n" 

    panelStep = Panel(
        stepContent,
        border_style="bright_black",
        box=box.ROUNDED,
        padding=(2, 0, 0, 2)
    )

    panelSearchStep = Panel(
        panelStep,
        title=f"\n[bold #4cbfc7] {titleText.upper()} INSTRUCTIONS [bold #4cbfc7]\n",
        title_align="center",
        box=box.MINIMAL,
        padding= (1,4,0,4)
    )

    console.print(panelSearchStep)
    console.print(Rule(style="#4cbfc7", characters="_"))
    
    
    while True:
        choice, error = choiceChecker(f"\n{'':<5}[red][b]SELECT 0 TO GO BACK [b][/red]")
        if error != "[bold red]INVALID INPUT! ENTER A NUMBER ONLY[/bold red]" and choice != 0:
            error = "[bold red]INVALID INPUT! ENTER A 0 ONLY[/bold red]"

        if error:
            return instructions(productIndex, material, searchResult, error)
        else:
            return 0



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info----------------------------------------------------FOR DISPLAYING THE PRODUCTS-----------------------------------------------------------------



def productList(matChoice, errorMessage=None):

    clearScreen()

    if errorMessage:
        panelError = Panel(
            errorMessage,
            border_style="red",
            box=box.ROUNDED,
            padding=(0, 2)
        )
        console.print(panelError)

    displayHeader()
    console.print(Rule(style="#4cbfc7", characters="_"))
    print("\n")
    
    productsInColumn = 3
    verticalProduct = []
    currentProduct = []

    for i in range(1, len(products[matChoice]) + 1):
        productPanel = Panel(
            f"[bold #4cbfc7][{i}].[/bold #4cbfc7] {products[matChoice][i]['title']}",
            border_style="bright_black", 
            box=box.ROUNDED, 
            padding=(0, 2),
            title_align="left"
        )

        currentProduct.append(productPanel)

        if i % productsInColumn == 0 or i == len(products[matChoice]):
            productGroup = Group(*currentProduct)
            verticalProduct.append(productGroup)
            currentProduct = []

    productsColumn = Columns(verticalProduct, equal=False, expand=True)

    panelProducts = Panel(
        productsColumn,
        title=f"\n[bold #4cbfc7]{matChoice.upper()} PRODUCT SELECTION [bold #4cbfc7]\n",
        title_align="center",
        box=box.MINIMAL,
        padding=(2,4,2,4)
    )

    console.print(panelProducts)
    console.print(Rule(style="#4cbfc7", characters="_"))

    while True:
        
        selectedProduct, error = choiceChecker(f"\n{'':<5}[#4cbfc7][b]SELECT YOUR CHOICE (O TO GO BACK) [b][/#4cbfc7]")
        
        if error:
            return productList(matChoice, error)
        
        if selectedProduct == 0:
            return 0 

        if selectedProduct > len(products[matChoice]):
            errorMessage = f"[bold red]INVALID INPUT! ENTER A NUMBER BETWEEN 0 - {len(products[matChoice])}![/bold red]"
            return productList(matChoice, errorMessage)
            
        return selectedProduct



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info----------------------------------------------------FOR DISPLAYING THE MATERIAL SELECTION-------------------------------------------------------



def materialList(errorMessage=None):

    materialNames = list(products.keys())

    clearScreen()
    
    if errorMessage:
        panelError = Panel(
            errorMessage,
            border_style="red",
            box=box.ROUNDED,
            padding=(0, 2)
        )
        console.print(panelError)

    displayHeader()
    console.print(Rule(style="#4cbfc7", characters="_"))
    print("\n")

    itemsInColumn = 5
    verticalColumns = []
    currentGroupItems = []
    
    for index, mat in enumerate(materialNames, start=1): 
        item_panel = Panel(
            f"[bold #4cbfc7][{index}].[/bold #4cbfc7] {mat}",
            border_style="bright_black", 
            box=box.ROUNDED, 
            padding=(0, 2),
            title_align="left"
        )

        currentGroupItems.append(item_panel)

        if index % itemsInColumn == 0 or index == len(materialNames):
            columnGroup = Group(*currentGroupItems)
            verticalColumns.append(columnGroup) 
            currentGroupItems = []

            
    materialColumns = Columns(verticalColumns, equal=False, expand=True)

    panelMaterial = Panel(
        materialColumns,
        title="\n[bold #4cbfc7]   MATERIAL SELECTION   [/bold #4cbfc7] \n",
        title_align="center",
        box=box.MINIMAL,
        padding=(2,4,2,4)
    )
    
    console.print(panelMaterial)
    console.print(Rule(style="#4cbfc7", characters="_"))

    while True:
        

        choice, error = choiceChecker(f"\n{'':<5}[#4cbfc7][b]SELECT YOUR CHOICE (0 TO GO BACK)[b][/#4cbfc7]")

        if error:
            return materialList(error)

        if choice == 0: 
            return
        if (choice > len(products)):
            errorMessage = f"[bold red]INVALID INPUT! ENTER A NUMBER BETWEEN 0 - {len(products)}![/bold red]"
            return materialList(errorMessage)
        else:
            loop = 1
            matChoice = None
            for mat in products:
                if loop == choice:
                    matChoice = mat
                    break
                loop += 1

            selectedProduct = productList(matChoice)

            if selectedProduct == 0:

                return materialList() 
            
            instructions(selectedProduct, matChoice, 0)
            return materialList() 



# #info------------------------------------------------------------------------------------------------------------------------------------------------
# # #end-info----------------------------------------------FOR DISPLAYING THE NAVIGATION MENU----------------------------------------------------------



def navigation(errorMessage=None):
    
    clearScreen()

    if errorMessage:
        panelError = Panel(
            errorMessage,
            border_style="red",
            box=box.ROUNDED,
            padding=(0, 2)
        )
        console.print(panelError)

    displayHeader()

    console.print(Rule(style="#4cbfc7 ", characters="_"))
    print("\n")

    navCon = [] 

    nav = [
        "Select material",
        "Search for Specific Product",
        "Add an Instruction",
        "Quit"
    ]



    for idxNav, navItem in enumerate(nav, start=1):

        panelShowNav = Panel(
            f"[bold #4cbfc7][{idxNav}].[/bold #4cbfc7] {navItem.upper()}",
            border_style="bright_black",
            padding=(0, 2),
        )
        navCon.append(panelShowNav)
        showNav = Group(*navCon)

    panelNav = Panel(
        Align.center(showNav),
        title="\n[bold #4cbfc7] NAVIGATION MENU [/bold #4cbfc7]\n",
        title_align="center",
        box=box.MINIMAL,
        padding=(1, 4)
    )

    console.print(panelNav)
    console.print(Rule(style="#4cbfc7 ", characters="_"))
    
    while True:
        navChoice, error = choiceChecker(f"\n{'':<5}[#4cbfc7][b]SELECT YOUR CHOICE [b][/#4cbfc7]")
        
        if error:
            return navigation(error)
        
        if navChoice > len(nav):
            errorMessage = f"[bold red]INVALID INPUT! ENTER A NUMBER BETWEEN 0 - {len(nav)}![/bold red]"
            return navigation(errorMessage)

        return navChoice



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------FOR DISPLAYING THE SEARCH RESULT-----------------------------------------------------------------



def showSearchResult(find, searchResult, errorMessage=None):

    clearScreen()
    
    if errorMessage:
        panelError = Panel(
            errorMessage,
            border_style="red",
            box=box.ROUNDED,
            padding=(0, 2)
        )
        console.print(panelError)

    displayHeader()
    
    panelShowSearch = Panel(
            Align.center(f"[bold #4cbfc7]RESULTS FOR: {find.upper()}[/bold #4cbfc7]"),
            border_style="#4cbfc7 on #001515",
            box=box.ROUNDED, 
            padding=(0, 3)
        )

    console.print(panelShowSearch)
    print("\n")

    
    index = 1
    for results in searchResult:
        showshow = (f"{index}. {results}")
        index += 1

        panelShow = Panel(
            showshow,
            border_style="bright_black",
            padding=(0, 0, 0, 3)
        )

        console.print(panelShow)

    
    console.print(Rule(style="#4cbfc7", characters="_"))

    while True:
        searchChoice, error = choiceChecker(f"\n{'':<5}[#4cbfc7][b]SELECT YOUR CHOICE (0 TO GO BACK) [b][/#4cbfc7]")

        if error:
            return showSearchResult(find, searchResult, error)

        if searchChoice == 0:
            return 0

        if searchChoice > len(searchResult):
            errorMessage = f"[bold red]INVALID INPUT! ENTER A NUMBER BETWEEN 0 - {len(searchResult)}![/bold red]"
            return showSearchResult(find, searchResult, errorMessage)

        selected = searchResult[searchChoice - 1]
        return selected



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------FOR DISPLAYING THE SEARCH SCREEN-----------------------------------------------------------------


    
def searchProduct():
    while True:
        panelSearch = Panel(
            Align.center(f"[bold white] PRODUCT SEARCH [/bold white]"),
            border_style="#4cbfc7 on #001515",
            box=box.ROUNDED,
            padding=(0, 2)
        )

        clearScreen()
        displayHeader()
        console.print(Rule(style="#4cbfc7", characters="_"))
        console.print(panelSearch)
        console.print(Rule(style="#4cbfc7", characters="_"))
        print("\n")

        find = Prompt.ask(f"{'':<5}[bold #4cbfc7]SEARCH FOR[/bold #4cbfc7]")
        if find == '0':
            return None, None
        if find == '': pass
        else: break

    searchResult = []
    for material in products:
        for productIndex in products[material]:
            if re.search(find, products[material][productIndex]['title'].casefold()):
                searchResult.append(products[material][productIndex]['title'])

    return find, searchResult



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------FOR DISPLAYING THE OPTION 3-----------------------------------------------------------------



def AddInstruction(errorMessage=None):
    
    clearScreen()

    if errorMessage:
        panelError = Panel(
            errorMessage,
            border_style="red",
            box=box.ROUNDED,
            padding=(0, 2)
        )
        console.print(panelError)

    displayHeader()
    console.print(Rule(style="#4cbfc7", characters="_"))
    
    panelLogin = Panel(
        Align.center("[bold #4cbfc7]ADMIN LOGIN REQUIRED[/bold #4cbfc7]"),
        border_style="#4cbfc7",
        box=box.ROUNDED,
        padding=(0, 2)
    )
    console.print(panelLogin)
    console.print(Rule(style="#4cbfc7", characters="_"))
    print("\n")
    
    user = Prompt.ask(f"{'':<5}[bold white]Username[/bold white]", console=console)
    pw = getpass(f"{'':<5}Password: ") 
   
        
    if user == "admin" and pw == '1234':
        
        while True:
            clearScreen()
            displayHeader()

            panelAddTitle = Panel(
                Align.center("[bold #4cbfc7]ADD NEW CRAFTING INSTRUCTION[/bold #4cbfc7]"),
                border_style="#4cbfc7",
                box=box.ROUNDED,
                padding=(0, 2)
            )
            console.print(panelAddTitle)
            console.print(Rule(style="#4cbfc7", characters="_"))
            print("\n")

            nMat = Prompt.ask(f"{'':<5}[bold #4cbfc7]ENTER MATERIAL CATEGORY[/bold #4cbfc7]")
            nTitle = Prompt.ask(f"{'':<5}[bold #4cbfc7]PRODUCT TITLE[/bold #4cbfc7]")
            
            console.print(Rule(style="#4cbfc7", characters="_"))
            panelMaterialsGuide = Panel(
                f"Enter materials, one by one. Type DONE when finished.".upper(),
                border_style="bright_black",
                box=box.ROUNDED,
                padding=(0, 1)
            )
            console.print(panelMaterialsGuide)
            
            materialsList = []
            materialCount = 1
            while True:
                material = Prompt.ask(f"[bold #4cbfc7][MATERIAL {materialCount}.][/bold #4cbfc7]")
                if material.upper() == 'DONE':
                    break
                materialsList.append(material)
                materialCount += 1
                
            console.print(Rule(style="#4cbfc7", characters="_"))
            panelToolsGuide = Panel(
                f"Enter tools needed, one by one. Type DONE when finished.".upper(),
                border_style="bright_black",
                box=box.ROUNDED,
                padding=(0, 1)
            )
            console.print(panelToolsGuide)
            
            toolsList = []
            toolCount = 1
            while True:
                tool = Prompt.ask(f"[bold #4cbfc7][TOOL {toolCount}.][/bold #4cbfc7]")
                if tool.upper() == 'DONE':
                    break
                toolsList.append(tool)
                toolCount += 1
            
            
            console.print(Rule(style="#4cbfc7", characters="_"))
            panelStepsGuide = Panel(
                f"Enter Instructions step-by-step. Type DONE when finished.".upper(),
                border_style="bright_black",
                box=box.ROUNDED,
                padding=(0, 1)
            )
            console.print(panelStepsGuide)
            
            stepsList = []
            stepCount = 1
            while True:
                step = Prompt.ask(f"[bold #4cbfc7][STEP {stepCount}.][/bold #4cbfc7]")
                if step.upper() == 'DONE':
                    break
                stepsList.append(step)
                stepCount += 1
            
            if not nMat or not nTitle or not stepsList:
                panelCancel = Panel(
                    "[bold red]INCOMPLETE DATA. PLEASE RESTART.[/bold red]",
                    border_style="red",
                    box=box.ROUNDED
                )
                console.print("\n")
                console.print(panelCancel)
                Prompt.ask("PRESS ENTER TO RETURN TO MENU")
                return

            nMatKey = nMat.casefold()

            if nMatKey not in products:
                products[nMatKey] = {}
                nextKey = 1
            else:
                existingKeys = [k for k in products[nMatKey].keys() if isinstance(k, int)]
                nextKey = max(existingKeys) + 1 if existingKeys else 1


            products[nMatKey][nextKey] = {
                "title": nTitle,
                "materials": materialsList,
                "tools": toolsList,
                "steps": stepsList 
            }
            
            try:
                def converterStr(data):
                    if isinstance(data, dict):
                        return {str(k): converterStr(v) for k, v in data.items()}
                    elif isinstance(data, list):
                        return [converterStr(item) for item in data]
                    else:
                        return data

                products_for_save = converterStr(products)

                with open('products.json', 'w') as f:
                    json.dump(products_for_save, f, indent=4)
                
                console.print(Rule(style="green", characters="-"))
                clearScreen()
                displayHeader()
                panelSaveSuccess = Panel(
                    Align.center(f"INSTRUCSTIONS FOR '{nTitle.upper()}' ADDED SUCCESSFULLY!"),
                    border_style="#4cbfc7 on #001515",
                    box=box.ROUNDED,
                    padding=(0, 2)
                )
                console.print(panelSaveSuccess)
                break 

            except Exception as e:
                panelSaveError = Panel(
                    f"[bold red]Error saving to file: {e}[/bold red]",
                    border_style="red",
                    box=box.ROUNDED
                )
                console.print(panelSaveError)
                break

    else:

        login_error = "[bold red]INVALID USERNAME OR PASSWROD[/bold red]"
        return AddInstruction(login_error)

    Prompt.ask("\nPRESS ENTER TO RETURN TO MENU")



## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------FOR MAIN FUNCTION-----------------------------------------------------------------------------



def main():
    while True:

        navChoice = navigation() 
        if navChoice == 0:
             continue
        match navChoice:

            case 1:
                materialList()

            case 2:
                find, search_results = searchProduct()
                
                if find is None:
                    continue
                
                if not search_results:
                    clearScreen()
                    displayHeader()
                    panelNoResults = Panel(
                        Align.center(f"[bold red]NO RESULTS FOUND FOR: {find.upper()}[/bold red]"),
                        border_style="red",
                        box=box.ROUNDED
                    )
                    console.print("\n")
                    console.print(panelNoResults)
                    Prompt.ask("\nPRESS ENTER TO RETURN TO MENU")
                    continue


                searchSelect = showSearchResult(find, search_results)
                
                if searchSelect == 0:
                    continue

                result=instructions(0, 0, searchSelect)
                if result == 0:
                    continue
                
            
            case 3:
                AddInstruction()
                
            
            case 4:
                panelEnding = Panel(
                    Align.center("[bold #4cbfc7]THANK YOU FOR USING THE RECYCLE CRAFTING MENU![/bold #4cbfc7]"),
                    border_style="#4cbfc7",
                    box=box.ROUNDED,
                    padding=(1, 2)
                )
                clearScreen()
                displayHeader()
                console.print(panelEnding)
                break
            
            case _:
                pass


## #info------------------------------------------------------------------------------------------------------------------------------------------------
## #info-------------------------------------------------TAPOS NAAA-----------------------------------------------------------------


main()