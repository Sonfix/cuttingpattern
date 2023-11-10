import json
from django.http import JsonResponse
import os

from .models import Customer, CustomerGroup, CuttingPattern
from .EDI.edi import EdiFile
from .EDI.Hopti_handler import *


TEST_DATA = "D:\\_VMShare\\Dev_CPP\\00_Kunden\\FR, Auvergne\\20210902\\37.EDI5"

class Api():

    def __init__(self):
        self.command_list = {
            "get_cutting_pattern" : self.get_cutting_pattern,
            "add_cutting_pattern" : self.add_cutting_pattern,
            "get_customers" : self.get_customers,
            "delete_pattern" : self.delete_pattern,
            "get_customer_groups" : self.get_customer_groups,
            "get_machine_code" : self.get_machine_code,
            "get_header_information" : self.get_header_information,
            "test_dll" : self.test_dll,
        }

    def resolve_command(self, command, request):
        if command in self.command_list:
            if request.method != "POST":
                return JsonResponse({
                    "result" : False
                }, status=405)

            return self.command_list[command](request)
        else:
            return JsonResponse({
                "result" : False,
                "error" : "Command is not defined!"
            }, status=404)

    
    def get_cutting_pattern(self, request):
        '''
            gets the cutting pattern form db
            also translates the machine code to json if it is not in db
        '''

        data = json.loads(request.body)

        cp = CuttingPattern.objects.get(pk=data.get("id"))
        #if not cp.exists():
        #    return JsonResponse({
        #        "result" : False,
        #        "message": "CuttingPattern does not exist!"
        #    })

        json_data = cp.json_file
        if not json_data:
            json_data = EdiFile().ImportFromEdiFile(cp.machine_code).ExportToJson()
            cp.json_file = json_data
            cp.save()
        
        return JsonResponse({
            "result" : True,
            "file" :  json_data
            }, status=200)
    
    def add_cutting_pattern(self, request):
        '''
            adds the given cuttingpattern to db
        '''
        data = json.loads(request.body)

        file_name = data.get("file_name")
        description = data.get("description")
        machine_code = data.get("machine_code")

        customer_name = data.get("customer")
        customer_group = data.get("customer_group")

        if customer_group:
            group = CustomerGroup.objects.filter(name = customer_group)
            if not group.exists():
                group = CustomerGroup(
                    name = customer_group
                )
                group.save()


        customer = Customer.objects.filter(name = customer_name)
        if not customer.exists():
            if group:
                customer = Customer(
                    name = customer_name,
                    group = group
                )
            else:
                customer = Customer(
                    name = customer_name
                )
            customer.save()
        else:
            customer = customer.first()
        
        json_data = EdiFile().ImportFromEdiFile(machine_code).ExportToJson()
        cp = CuttingPattern(
            file_name = file_name,
            description = description,
            machine_code = machine_code,
            json_file = json_data,
            user = request.user,
            customer = customer
        )
        
        res = False
        if cp:
            res = True
            cp.save()

        return JsonResponse({
            "result" : res,
            "id" : cp.id
        }, status=201)


    def get_customers(self, request):
        res = []
        for c in Customer.objects.all():
            res.append(c.name)

        return JsonResponse({
            "result" : True,
            "customers" : res
        }, status=201)

    def delete_pattern(self, request):
        data = json.loads(request.body)

        id = data.get("id")
        cp = CuttingPattern.objects.get(pk=id)
        res = False
        if cp.user == request.user:
            cp.delete()
            res = True
        
        return JsonResponse({
            "result" : res
        }, status=201)

    def get_customer_groups(self, request):
        res = []
        for c in CustomerGroup.objects.all():
            res.append(c.name)

        return JsonResponse({
            "result" : True,
            "groups" : res
        }, status=200)


    def get_machine_code(self, request):
        data = json.loads(request.body)

        id = data.get("id")
        res = True
        machine_code = ""
        cp = CuttingPattern.objects.get(pk=id)
        if not cp:
            res = False
        else:
            machine_code = cp.machine_code
        
        return JsonResponse({
            "result" : res,
            "code" : machine_code,
            "name": cp.file_name
        }, status=200)

    def get_header_information(self, request):
        data = json.loads(request.body)

        id = data.get("id")
        res = True
        cp = CuttingPattern.objects.get(pk=id)
        json_data = {}
        if not cp:
            res = False
        else:
            json_data = EdiFile().ImportFromEdiFile(cp.machine_code).Header.exportToJson()
        
        return JsonResponse({
            "result" : res,
            "data" : json_data
        }, status=200)


    def test_dll(seld, request):
        # get the current working directory
        current_working_directory = os.getcwd()

        # print output to the console
        print(current_working_directory)
        hopti = HOpti_Handler()        
