#!/usr/bin/env python
# coding: utf-8

# In[27]:


from botData import chat_id_var, token_var
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
import pandas as pd
import telepot


# In[28]:


dados_login = pd.read_csv("login.csv",header=None)
dados_login.index = ['usuario','senha']
dados_login.columns = ['dados']


# In[29]:


options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": })
driver = webdriver.Chrome(options=options)
driver.get("https://sig.cefetmg.br/sigaa/verTelaLogin.do")
driver.implicitly_wait(3)
usuario_input = driver.find_element(by=By.NAME, value="user.login")
senha_input = driver.find_element(by=By.NAME, value="user.senha")
entrar_button = driver.find_element(by=By.CSS_SELECTOR, value="input[type='submit'], input[type='button']")


# In[30]:


try:
    cookie_button = driver.find_element(by=By.TAG_NAME, value="button")
    cookie_button.click()
except:
    print('cookie_button nao existe')


# In[31]:


usuario_input.send_keys(dados_login.loc['usuario'][0])
senha_input.send_keys(dados_login.loc['senha'][0])


# In[32]:


entrar_button.click()


# In[33]:


driver.implicitly_wait(3)
tabela_menu = driver.find_element(by=By.CLASS_NAME,  value="ThemeOfficeMenu")
ensino_menu = tabela_menu.find_elements(by=By.XPATH, value='.//td')[0]


# In[34]:


driver.implicitly_wait(3)
action = ActionChains(driver)
action.move_to_element(ensino_menu)
action.perform()
action.move_to_element_with_offset(ensino_menu, 0, 25)
action.click()
action.perform()


# In[35]:


driver.implicitly_wait(3)
pagina_notas = driver.page_source
list_of_dfs = pd.read_html(pagina_notas, header=None)


# In[36]:


driver.quit()


# In[37]:


unwanted_dfs = [0,1,len(list_of_dfs)-1]
list_of_dfs = [element for idx, element in enumerate(list_of_dfs) if idx not in unwanted_dfs]
df = pd.concat(list_of_dfs)
df_antigo = pd.read_csv('notas.csv',index_col=0)


# In[38]:


atualizacao = not(df.equals(df_antigo))
df.to_csv('notas.csv')
if atualizacao:
    df_diff = pd.concat([df, df_antigo]).drop_duplicates(keep=False,ignore_index=True)
    disciplina = df_diff.loc[0]['Disciplina']
    bot = telepot.Bot(token=token_var)
    bot.sendMessage(chat_id=chat_id_var, text='Atualização de nota em '+disciplina)


# In[ ]:




