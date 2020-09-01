#!/usr/bin/env python
# coding: utf-8

# In[2]:


import glob


# In[3]:


glob.glob("*.srt")


# In[10]:


with open(glob.glob("*.srt")[0], 'r') as f:
    text = f.readlines()
    
name = glob.glob("*.srt")[0].split(".")
name[-1] = "md"
name = ".".join(name)
print(name)
result = []
for t in text:
    if not t[0].isdigit() and t != "\n":
        t = t.replace("\n", " ")
        result.append(t)
        
with open(name, 'w') as f:
    f.write("".join(result))


# In[ ]:




