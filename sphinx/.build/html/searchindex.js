Search.setIndex({docnames:["backend","damage_models","database_interactions","delphin_interactions","delphin_parser","delphin_permutations","delphin_setup","file_parsing","general_interactions","index","inputs","material_interactions","material_parser","sampling","sampling_interactions","sampling_sampling","sampling_worker","simulation_interactions","simulation_worker","sobol_lib","weather_interactions","weather_modelling","weather_parser"],envversion:53,filenames:["backend.rst","damage_models.rst","database_interactions.rst","delphin_interactions.rst","delphin_parser.rst","delphin_permutations.rst","delphin_setup.rst","file_parsing.rst","general_interactions.rst","index.rst","inputs.rst","material_interactions.rst","material_parser.rst","sampling.rst","sampling_interactions.rst","sampling_sampling.rst","sampling_worker.rst","simulation_interactions.rst","simulation_worker.rst","sobol_lib.rst","weather_interactions.rst","weather_modelling.rst","weather_parser.rst"],objects:{"delphin_6_automation.backend":{sampling_worker:[16,0,0,"-"],simulation_worker:[18,0,0,"-"]},"delphin_6_automation.backend.sampling_worker":{main:[16,1,1,""],sampling_overview:[16,1,1,""],sampling_worker:[16,1,1,""]},"delphin_6_automation.backend.simulation_worker":{create_submit_file:[18,1,1,""],get_average_computation_time:[18,1,1,""],github_updates:[18,1,1,""],hpc_worker:[18,1,1,""],local_worker:[18,1,1,""],simulation_worker:[18,1,1,""],solve_delphin:[18,1,1,""],submit_job:[18,1,1,""],wait_until_finished:[18,1,1,""]},"delphin_6_automation.database_interactions":{delphin_interactions:[3,0,0,"-"],general_interactions:[8,0,0,"-"],material_interactions:[11,0,0,"-"],sampling_interactions:[14,0,0,"-"],simulation_interactions:[17,0,0,"-"],weather_interactions:[20,0,0,"-"]},"delphin_6_automation.database_interactions.delphin_interactions":{add_sampling_dict:[3,1,1,""],change_entry_kirchhoff_potential:[3,1,1,""],change_entry_simulation_length:[3,1,1,""],change_entry_solver_relative_tolerance:[3,1,1,""],check_delphin_file:[3,1,1,""],download_delphin_entry:[3,1,1,""],download_result_files:[3,1,1,""],upload_delphin_dict_to_database:[3,1,1,""],upload_delphin_to_database:[3,1,1,""],upload_processed_results:[3,1,1,""],upload_results_to_database:[3,1,1,""]},"delphin_6_automation.database_interactions.general_interactions":{add_to_simulation_queue:[8,1,1,""],does_simulation_exists:[8,1,1,""],download_full_project_from_database:[8,1,1,""],download_raw_result:[8,1,1,""],is_simulation_finished:[8,1,1,""],list_finished_simulations:[8,1,1,""],list_materials:[8,1,1,""],list_weather_stations:[8,1,1,""],queue_priorities:[8,1,1,""]},"delphin_6_automation.database_interactions.material_interactions":{change_material_location:[11,1,1,""],download_materials:[11,1,1,""],find_material_ids:[11,1,1,""],get_material_info:[11,1,1,""],list_project_materials:[11,1,1,""],upload_material_file:[11,1,1,""],upload_materials_from_folder:[11,1,1,""]},"delphin_6_automation.database_interactions.sampling_interactions":{add_delphin_to_sampling:[14,1,1,""],add_raw_samples_to_strategy:[14,1,1,""],add_sample_to_strategy:[14,1,1,""],get_delphin_for_sample:[14,1,1,""],get_sampling_strategy:[14,1,1,""],upload_raw_samples:[14,1,1,""],upload_sample_iteration_parameters:[14,1,1,""],upload_sample_mean:[14,1,1,""],upload_sample_std:[14,1,1,""],upload_samples:[14,1,1,""],upload_sampling_strategy:[14,1,1,""],upload_standard_error:[14,1,1,""]},"delphin_6_automation.database_interactions.simulation_interactions":{clean_simulation_folder:[17,1,1,""],download_simulation_result:[17,1,1,""],find_next_sim_in_queue:[17,1,1,""],set_simulated:[17,1,1,""],set_simulating:[17,1,1,""],set_simulation_time:[17,1,1,""],wait_until_simulated:[17,1,1,""]},"delphin_6_automation.database_interactions.weather_interactions":{assign_indoor_climate_to_project:[20,1,1,""],assign_weather_by_name_and_years:[20,1,1,""],assign_weather_to_project:[20,1,1,""],change_weather_file_location:[20,1,1,""],concatenate_weather:[20,1,1,""],download_weather:[20,1,1,""],list_project_weather:[20,1,1,""],upload_weather_to_db:[20,1,1,""]},"delphin_6_automation.delphin_setup":{damage_models:[1,0,0,"-"],delphin_permutations:[5,0,0,"-"],weather_modeling:[21,0,0,"-"]},"delphin_6_automation.delphin_setup.damage_models":{algae:[1,1,1,""],frost_curves:[1,1,1,""],frost_risk:[1,1,1,""],mould_index:[1,1,1,""],mould_pj:[1,1,1,""],u_value:[1,1,1,""],wood_rot:[1,1,1,""]},"delphin_6_automation.delphin_setup.delphin_permutations":{change_boundary_coefficient:[5,1,1,""],change_layer_material:[5,1,1,""],change_layer_width:[5,1,1,""],change_layer_widths:[5,1,1,""],change_orientation:[5,1,1,""],change_simulation_length:[5,1,1,""],change_weather:[5,1,1,""],compute_vapour_diffusion_slope:[5,1,1,""],convert_discretization_to_list:[5,1,1,""],discretize_layer:[5,1,1,""],get_layers:[5,1,1,""],get_simulation_length:[5,1,1,""],identify_layer:[5,1,1,""],update_assignment_range:[5,1,1,""],update_output_locations:[5,1,1,""],update_range_of_assignments:[5,1,1,""]},"delphin_6_automation.delphin_setup.weather_modeling":{convert_weather_to_indoor_climate:[21,1,1,""],driving_rain:[21,1,1,""],en13788:[21,1,1,""],en15026:[21,1,1,""],short_wave_radiation:[21,1,1,""]},"delphin_6_automation.file_parsing":{delphin_parser:[4,0,0,"-"],material_parser:[12,0,0,"-"],weather_parser:[22,0,0,"-"]},"delphin_6_automation.file_parsing.delphin_parser":{cvode_stats_to_dict:[4,1,1,""],d6o_to_dict:[4,1,1,""],dict_to_cvode_stats_file:[4,1,1,""],dict_to_d6o:[4,1,1,""],dict_to_g6a:[4,1,1,""],dict_to_les_stats_file:[4,1,1,""],dict_to_progress_file:[4,1,1,""],dp6_to_dict:[4,1,1,""],g6a_to_dict:[4,1,1,""],les_stats_to_dict:[4,1,1,""],progress_to_dict:[4,1,1,""],write_log_files:[4,1,1,""]},"delphin_6_automation.file_parsing.material_parser":{MyNumber:[12,2,1,""],dict_to_m6:[12,1,1,""],material_file_to_dict:[12,1,1,""]},"delphin_6_automation.file_parsing.weather_parser":{ccd_to_list:[22,1,1,""],dict_to_ccd:[22,1,1,""],list_to_ccd:[22,1,1,""],wac_to_dict:[22,1,1,""]},"delphin_6_automation.sampling":{inputs:[10,0,0,"-"],sampling:[15,0,0,"-"],sobol_lib:[19,0,0,"-"]},"delphin_6_automation.sampling.inputs":{construct_delphin_reference:[10,1,1,""],construct_design_files:[10,1,1,""],construction_types:[10,1,1,""],delphin_templates:[10,1,1,""],implement_insulation_widths:[10,1,1,""],implement_system_materials:[10,1,1,""],insulation_systems:[10,1,1,""],insulation_type:[10,1,1,""],plaster_materials:[10,1,1,""],wall_core_materials:[10,1,1,""]},"delphin_6_automation.sampling.sampling":{calculate_error:[15,1,1,""],calculate_sample_output:[15,1,1,""],check_convergence:[15,1,1,""],compute_sampling_distributions:[15,1,1,""],create_delphin_projects:[15,1,1,""],create_samples:[15,1,1,""],create_sampling_strategy:[15,1,1,""],get_raw_samples:[15,1,1,""],initialize_sampling:[15,1,1,""],load_design_options:[15,1,1,""],load_latest_sample:[15,1,1,""],load_strategy:[15,1,1,""],relative_standard_error:[15,1,1,""],sample_exists:[15,1,1,""],sobol:[15,1,1,""]},"delphin_6_automation.sampling.sobol_lib":{i4_bit_hi1:[19,1,1,""],i4_bit_lo0:[19,1,1,""],i4_sobol:[19,1,1,""],i4_sobol_generate:[19,1,1,""],i4_uniform:[19,1,1,""],isprime:[19,1,1,""],prime_ge:[19,1,1,""],scramble:[19,1,1,""],scrambled_sobol_generate:[19,1,1,""],sobol_generate:[19,1,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class"},terms:{"0x000001ad7ae46dd8":3,"0x000001ad7c662898":[3,11],"0x000001aee6c03fd0":[],"0x000001aee6c8ab38":[],"0x000001e69fd01630":[],"0x000001e69fd8c5f8":[],"0x0000025aa1f9f9b0":[],"0x0000025aa2025978":[],"class":[1,12,20,21],"default":3,"float":[1,5,15,19,21],"function":[1,15,19,21],"gr\u00fcnewald":1,"h\u00f8jskole":21,"int":[1,3,4,5,8,10,11,14,15,18,19,21],"new":[5,10,15,16,18,19],"return":[1,3,4,5,8,10,11,12,14,15,17,18,19,20,21,22],"short":21,"solstr\u00e5l":21,"true":[3,4,8,12,15,17,18,19,22],"while":5,AND:9,BUT:9,FOR:9,IDs:10,NOT:9,THE:9,The:[5,9,15,19],Then:18,USE:9,WITH:9,abov:9,accept:19,accord:10,acm:19,action:9,adapt:19,add:[3,8,14],add_delphin_to_sampl:14,add_raw_samples_to_strategi:14,add_sample_to_strategi:14,add_sampling_dict:3,add_to_simulation_queu:8,aed_group:1,after:[5,12,21],air:21,akad:19,albedo:[],alga:1,algorithm:19,all:[3,5,7,8,9,10,16,17],allen:19,alreadi:15,alwai:19,amount:10,analysi:[15,19],ani:9,antonov:19,appli:[1,10],appropri:19,area:1,aris:[9,10],arrai:[1,21],assign:[5,20],assign_indoor_climate_to_project:20,assign_weather_by_name_and_year:20,assign_weather_to_project:20,assignment_list:[],associ:[9,15,20],author:[9,19],autom:[15,18],avail:[10,18],averag:[18,21],backend:[9,16,18],balance_equation_modul:[],bank:19,base:[3,11,15,16,19,21],been:19,beheatmoistur:[],bennett:19,between:[1,5,19],binari:19,bit:19,blocken:21,bool:[3,4,8,12,15,17,18,19,20,22],bound:19,boundari:5,boundary_condit:5,bratlei:19,build:[1,21],built:21,burkardt:19,calcul:[1,15,21],calculate_error:15,calculate_sample_output:15,calculation_method:21,call:[15,19],can:[5,20,21],carlo:15,carmeliet:21,catch_ratio:21,ccd:22,ccd_to_list:22,cell:5,chan:19,chang:[3,5,11,20],change_boundary_coeffici:5,change_entry_kirchhoff_potenti:3,change_entry_simulation_length:3,change_entry_solver_relative_toler:3,change_kirchhoff_potenti:[],change_layer_materi:5,change_layer_width:5,change_material_loc:11,change_orient:5,change_simulation_length:5,change_solver_relative_toler:[],change_weath:5,change_weather_file_loc:20,charg:9,check:[3,8,15,16,19],check_converg:15,check_delphin_fil:3,chisari:19,chosen:19,christian:9,claim:9,clean:17,clean_simulation_fold:17,climat:[5,20,21],climate_class:20,climate_data_path:[],climate_databas:[],code:19,coeffici:5,coefficient_list:[],coefficient_nam:[],collect:15,color:5,comment:[],comput:[1,5,15,19],computation_tim:[17,18],compute_sampling_distribut:15,compute_vapour_diffusion_slop:5,concaten:20,concatenate_weath:20,condit:[5,9],connect:[9,14,15],construct:18,construct_delphin_refer:10,construct_design_fil:10,construction_typ:10,contain:[1,3,5,22],content:[0,2,6,7,9,13,17],continent:21,continu:18,contract:9,converg:16,convert:[3,4,12,22],convert_discretization_to_list:5,convert_weather_to_indoor_clim:21,copi:9,copyright:9,core:[1,10],corrado:19,correctli:5,cover:10,creat:[5,15,16,18],create_assign:[],create_attribut:[],create_condit:[],create_delphin_fil:[],create_delphin_project:15,create_directory_placehold:[],create_discret:[],create_init:[],create_materi:[],create_output:[],create_project_info:[],create_sampl:15,create_sampling_strategi:15,create_submit_fil:18,create_xml:[],critic:1,cube:19,current:[1,8,14,15],current_error:14,curv:1,cvode:4,cvode_stats_to_dict:4,d6o_to_dict:4,daili:21,daily_temperature_averag:21,daily_temperature_average_:21,damag:9,damage_model:1,danmark:21,data:22,databas:[3,4,8,9,11,14,15,17,18,20],database_interact:[3,4,8,11,14,15,17,20],datafram:10,dataset:19,datetim:[4,17],db_templat:[3,4,11,14,15,20],deal:9,decai:1,delet:3,delete_fil:3,delphin6fil:[],delphin:[2,7,8,10,11,14,15,16,17,18,20,22],delphin_6_autom:[1,3,4,5,8,10,11,12,14,15,16,17,18,19,20,21,22],delphin_dict:[3,5,10],delphin_docu:[3,11,20],delphin_entri:[3,11,20],delphin_ex:18,delphin_fil:[3,8],delphin_id:[3,14,17,20],delphin_interact:3,delphin_object:11,delphin_pars:4,delphin_permut:5,delphin_setup:[1,5,21],delphin_templ:10,delphinsolv:18,delta_rang:5,descript:22,design:[10,15],deviat:[14,15],dict:[3,4,5,8,10,11,12,14,15,20,21,22],dict_to_ccd:22,dict_to_cvode_stats_fil:4,dict_to_d6o:4,dict_to_g6a:4,dict_to_les_stats_fil:4,dict_to_m6:12,dict_to_progress_fil:4,dictionari:[1,4,10],differ:[1,10],diffus:5,digit:12,dim_num:19,dimens:[15,19],discret:5,discretiz:5,discretize_lay:5,discuss:19,distribut:[9,19,21],divis:5,document:20,document_id:8,does_simulation_exist:8,done:16,download:[8,11,14,17,20],download_delphin_entri:3,download_full_project_from_databas:8,download_materi:11,download_path:[3,4,8,17],download_raw_result:8,download_result_fil:3,download_simulation_result:17,download_weath:20,dp6_to_dict:4,draw_back:1,drive:21,driving_rain:21,dth:21,dtu:18,due:1,dummi:1,durat:[],duration_unit:[],each:[1,5,15,19],ecuy:19,edit:19,effcienc:15,effici:19,either:[17,20,21],element:[5,19],els:18,empti:15,en13788:21,en15026:21,end:18,engin:15,entranc:16,entri:[3,4,8,11,14,15,17,18,20],equal:19,error:[14,15],essenti:19,estim:[15,18],estimated_run_tim:18,eur:1,eval:1,evalu:1,event:9,exampl:19,exce:1,excel_fil:10,exchang:5,exe:18,exist:15,express:9,extens:4,exterior_temperatur:1,fals:[3,8,15,17,18,19],februari:19,field:[3,11],file:[3,4,5,8,9,10,11,12,15,18,20,22],file_attribut:[],file_dict:4,file_pars:[4,12,22],file_path:[12,20,22],filenam:4,find:[11,17],find_material_id:11,find_next_sim_in_queu:17,finish:17,first:19,fit:[9,15],flag:17,folder:[3,4,8,10,11,15,17,18,20,22],follow:[5,9,22],fortran77:19,found:[5,17],fox:19,frame:10,free:9,from:[3,5,8,9,10,15,17,18,20,22],frost:1,frost_curv:1,frost_risk:1,full:22,furnish:9,g6a_to_dict:4,gener:[2,9,10,15,19],general_interact:[8,18],geometri:4,geometry_dict:4,geometry_file_hash:4,geometry_file_nam:4,get:[5,10,11,14,18],get_average_computation_tim:18,get_delphin_for_sampl:14,get_delphin_project_dimens:[],get_git_revision_hash:18,get_github_vers:18,get_lay:5,get_material_info:11,get_raw_sampl:15,get_sampling_strategi:14,get_simulation_length:5,github:18,github_upd:18,given:[1,5,11,14,15,16,17],gnu:19,goodman:19,grant:9,greater:19,growth:1,guid:19,handbook:19,handl:[0,2,6,7,13],has:[5,17,19],hash:4,hatchcod:5,have:[5,12],heat:1,heat_loss:1,heat_slop:5,herebi:9,high:[8,19],highest:17,hold:4,holder:9,hou:15,hourli:22,how:[1,15],hpc:18,hpc_worker:18,humid:21,hygrotherm:9,i4_bit_hi1:19,i4_bit_lo0:19,i4_sobol:19,i4_sobol_gener:19,i4_uniform:19,ibk:18,ibm:19,id_:[17,18],idea:19,identifi:5,identify_lay:5,ids:[11,17],ilya:19,implement:[1,10,19,21],implement_insulation_width:10,implement_system_materi:10,impli:[1,9],inclin:21,includ:[9,10],increas:5,index:[1,5,9,19],indic:1,indoor:[1,20,21],indoor_class:21,info:[11,18],inform:4,initi:[15,19],initialize_sampl:15,input:[9,13,19],input_fil:[10,15],instanc:5,insul:10,insulation_system:10,insulation_typ:10,insulationsystem:10,integ:[10,19],integrator_cvode_stat:4,interact:[0,9],interfac:[],interior_temperatur:1,interrupt:18,intersci:19,intro:22,ipm:19,is_prim:19,is_simulation_finish:8,isfloat:[],isprim:19,iter:[1,14,15,16,21],its:8,jame:19,jerri:19,job:18,john:[1,19],journal:19,json:15,keep:5,kei:[5,10,22],kind:9,kirchhoff:3,kongsgaard:9,laboratoriet:21,last:15,latitud:21,layer:[5,10],layer_materi:5,leap:19,length:[3,5],length_list:[],length_unit:5,les:4,les_direct_stat:4,les_stats_to_dict:4,less:19,levitan:19,lewi:19,lfv:21,lgpl:19,liabil:9,liabl:9,librari:[9,13],licens:19,limit:[1,9],linu:19,list:[1,4,5,8,10,11,14,15,17,19,20,21,22],list_finished_simul:8,list_materi:8,list_project_materi:11,list_project_weath:20,list_to_ccd:22,list_weather_st:8,literatur:1,load:[5,15,21],load_design_opt:15,load_latest_sampl:15,load_strategi:15,local:18,local_work:18,locat:[5,11,15,20],location_nam:22,log:4,log_path:4,logger:18,longitud:21,look:[5,15,18],loop:[10,15,18],loss:1,low:[1,8,19,21],lower:15,made:9,main:[16,18],make:12,makkonen:1,mani:15,mass:1,materi:[1,2,5,7,8,9,10,20],material_databas:[],material_file_to_dict:12,material_id:11,material_interact:11,material_numb:[],material_pars:12,material_path:11,mathemat:19,matlab:19,maximum:[5,19],maximum_divis:5,mean:[1,14,15],measur:[1,19],medium:8,member:[],memori:15,merchant:9,merg:9,meta:22,metadata:3,miller:19,minimum:19,minimum_divis:5,minut:18,model:[6,9,10],modif:6,modifi:[5,9,19],modul:[0,2,6,7,9,13],mold:1,mongo_db:22,mongoengin:[3,11],mont:15,moscow:19,mould:1,mould_index:1,mould_pj:1,much:1,multiarrai:1,multidimension:19,must:19,mynumb:12,name:[4,5,10,11,15,20],namedtupl:5,nauk:19,ndarrai:[1,14,15,21],neg:19,nest:5,new_discret:5,new_materi:5,new_orient:5,new_sampl:14,new_valu:5,new_weath:5,new_width:5,next:[17,19],nielsen:9,non:19,none:[3,4,5,11,14,15,16,17,18,21],nonetyp:[],noninfring:9,nonneg:19,notat:12,notic:9,num:[],number:[5,8,14,19],number_of_hour:4,numpi:[1,14,15,21],object:[3,11],objectidfield:[3,11],obtain:9,ocni:[10,15],ojanen:1,one:10,ones:[15,17],onli:[5,21],option:[4,10,15,17,18],orient:[5,21],orientation_list:[],origin:[5,19],original_id:[],original_materi:5,original_weath:5,other:9,otherwis:[8,9,15,17,18,19],out:[3,9,18],outdoor:[1,21],output:[1,5,19],output_fil:[],output_grid:[],output_unit:[],owen:19,page:[9,19],panda:10,param:1,paramet:[3,4,5,8,10,11,12,14,15,17,18,19,20,21,22],parameter_info:22,pars:9,parser:[7,9],particular:9,path:[3,4,5,8,11,12,15,17,22],path_:3,paul:19,per:15,perkov:9,permiss:9,permit:9,permut:[6,9,10],permutate_entry_boundary_coeffici:[],permutate_entry_layer_materi:[],permutate_entry_layer_width:[],permutate_entry_orient:[],permutate_entry_simulation_length:[],permutate_entry_weath:[],person:9,peter:19,physic:19,pierr:19,place:[12,22],plaster:10,plaster_materi:10,point:19,portion:9,posit:[1,19],possibl:12,potenti:3,precipit:21,preprint:19,press:21,previou:15,prime:19,prime_g:19,print_material_dict:[],print_weather_stations_dict:[],prioriti:[3,8,17],probabilist:13,process:[3,17],prod:1,product:19,program:[9,18],progress:[4,16],progress_to_dict:4,project:[3,4,5,6,8,9,11,14,15,16,17,18,20],project_materi:11,properti:1,provid:9,pseudo:19,pseudorandom:19,publish:9,purpos:9,pycharmproject:[10,15],python:[4,19],quasi:[15,19],quasirandom:19,queue:[3,8,17,18],queue_prior:[3,8],radiat:21,rain:21,random:19,randomli:19,rang:5,range_to_update_aft:5,raw:[3,14,15,17],raw_or_process:17,raw_result_id:3,reach:16,refer:19,reformat:10,rel:[3,15,19,21],rel_tol:3,relat:14,relative_humid:1,relative_humidity_list:1,relative_standard_error:15,relative_toler:[],relev:[1,10],reliabl:15,represent:4,request:19,research:9,restart:18,restrict:9,result:[3,4,8,14,15,17],result_dict:4,result_id:8,result_length:3,result_nam:[],result_obj:[3,4],result_path:4,result_raw_entri:[3,4],ribuild:18,right:9,rise:21,risk:1,rot:1,routin:19,rows_to_read:10,rst:[3,8,11,20],rtype:19,run:18,russian:19,safeti:15,saleev:19,saltelli:19,same:15,sampl:[0,2,3,9,10,19],sample_data:3,sample_entri:[14,15],sample_exist:15,sample_id:14,sample_iter:14,sample_mean:14,sample_std:14,sample_strategi:15,samples_raw:[14,15],samples_raw_id:14,sampling_id:15,sampling_interact:14,sampling_overview:16,sampling_strategi:[14,15],sampling_strategy_id:15,sampling_work:16,satisfi:19,save:[11,15,22],scale:19,schrage:19,scientif:12,scott:19,scrambl:19,scrambled_sobol_gener:19,script:9,search:9,seed:19,select:10,sell:9,sensit:[1,19],sensitivity_class:1,separ:10,sequenc:[15,19],sequence_length:15,sequence_numb:14,seri:[1,15],set:[15,17,19],set_simul:17,set_simulation_tim:17,set_to:[3,17],setup:9,shall:9,short_wave_radi:21,should:[3,4,5,8,12,15,17,19,22],show:16,sim_id:[3,8,17,18,20],sim_loc:18,simpli:19,simul:[0,2,3,4,5,8,9,13,14,15,16,19],simulation_fold:18,simulation_interact:17,simulation_interrupt:3,simulation_length:5,simulation_start:4,simulation_work:18,singl:5,size:5,skip:19,slope:5,smallest:[5,19],sobol:[9,13,15],sobol_gener:19,sobol_lib:19,softwar:[9,19],solv:18,solve_delphin:18,solver:3,sourc:[1,3,4,5,8,10,11,12,14,15,16,17,18,19,20,21,22],spatial:[19,21],springer:19,sssr:19,standard:[14,15],start:4,stat:4,station:8,step:[1,15],str:[3,4,5,8,10,11,12,14,15,16,17,18,20,21,22],strategi:[14,15,16],strategy_doc:[14,15],strategy_docu:[14,15],strategy_id:[14,16],stretch_factor:5,string:10,structur:[1,21],subdivid:5,subdivis:5,subject:9,sublicens:9,submit:18,submit_fil:18,submit_job:18,substanti:9,success:[17,18],summari:18,suppos:18,surface_qu:1,svendsen:21,system:[10,15,18,19],t_co:1,take:[12,22],techno:21,teknisk:21,temperatur:[1,21],temperature_list:1,templat:10,tempor:21,text:5,than:[15,19],thei:[5,15],them:3,therefor:5,thi:[0,2,6,7,9,13,18,19],thick:10,thoma:9,those:10,though:19,thread_nam:[],threshold:15,through:[10,15,18],time:[1,4,15,17,18],timedelta:17,titl:10,togeth:20,toler:3,took:17,toratti:1,tort:9,toward:1,transact:19,treat:19,tsv:4,tupl:[1,4,5,11,15,21],turn:4,two:1,type:[15,18,19],u_valu:1,uncertainti:15,under:[9,19],uniformli:19,union:[1,5,21],uniqu:11,unit:3,unit_list:[],univpm:1,until:[17,18],updat:[5,14,19],update_assignment_rang:5,update_output_loc:5,update_range_of_assign:5,update_short_wave_condit:[],upload:[3,8,11,14,20],upload_delphin_dict_to_databas:3,upload_delphin_to_databas:3,upload_material_fil:11,upload_materials_from_fold:11,upload_processed_result:3,upload_raw_sampl:14,upload_results_to_databas:3,upload_sampl:14,upload_sample_iteration_paramet:14,upload_sample_mean:14,upload_sample_std:14,upload_sampling_strategi:14,upload_standard_error:14,upload_weather_to_db:20,upper:1,use:9,used:[5,14,18],used_sampl:14,used_samples_per_set:15,user:[0,10,15],user_path_input:11,using:1,ussr:19,usual:19,val:12,valid:3,valu:[1,5,15,19,22],vapour:5,vapour_exchang:5,variat:10,varmeisol:21,vector:19,verbosity_level:18,verlag:19,version:[18,19],viitanen:1,volum:19,wac:[20,22],wac_to_dict:22,wait:17,wait_until_finish:18,wait_until_simul:17,wall:[10,21],wall_core_materi:10,wall_loc:21,warranti:9,wave:21,weather:[2,5,6,7,8,9],weather_dict:22,weather_docu:20,weather_interact:20,weather_list:22,weather_model:21,weather_pars:22,weather_st:[],weather_station_dict:[],weather_station_nam:20,were:[4,19],what:17,when:16,where:[1,3,8,12,15,18,22],whether:[9,15,17],which:[5,16,17],whom:9,width:5,wilei:19,wind:21,wind_direct:21,wind_spe:21,within:10,without:[9,10],wood:1,wood_rot:1,wooden:1,worker:[0,9],wp6:15,write:3,write_log_fil:4,write_xml:[],written:[3,4,8],x_index:5,x_width:5,year:[20,22],yet:17},titles:["RiBuild Backend","Weather Modeling","RiBuild Database Interactions","Delphin Interactions","Delphin Parser","Delphin Permutations","RiBuild Delphin Setup","RiBuild File Parsing","General Interactions","Welcome to RiBuild - Delphin Automation\u2019s documentation!","Inputs","Material Interactions","Material Parser","RiBuild Sampling","Sampling Interactions","Sampling","Sampling Worker","Simulation Interactions","Simulation Worker","Sobol Library","Weather Interactions","Weather Modeling","Weather Parser"],titleterms:{autom:9,backend:0,creat:[],databas:2,delphin:[3,4,5,6,9],delphin_6_autom:[],document:9,file:7,gener:8,indic:9,input:10,interact:[2,3,8,11,14,17,20],librari:19,licens:9,materi:[11,12],model:[1,21],pars:7,parser:[4,12,22],permut:5,ribuild:[0,2,6,7,9,13],sampl:[13,14,15,16],sampling_work:[],setup:6,simul:[17,18],simulation_work:[],sobol:19,sobol_lib:[],tabl:9,weather:[1,20,21,22],welcom:9,worker:[16,18]}})