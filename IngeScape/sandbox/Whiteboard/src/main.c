//
//  main.c
//  Whiteboard
//  Created by Ingenuity i/o on 2025/11/02
//
// no description
//

#ifdef _WIN32
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#define NOMINMAX
#include <windows.h>
#include <winsock2.h>
#endif

#include <ingescape/ingescape.h>


void myIOCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                   void* value, size_t valueSize, void* myData){
    igs_info("%s changed", name);

    //add code here if needed

}

void myServiceFunction(const char *callerAgentName, const char *callerAgentUUID,
                       const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                       const char *token, void* myData){
    igs_info("%s(%s) called %s", callerAgentName, callerAgentUUID, serviceName);

    //add code here if needed

}

int main(int argc, const char * argv[]) {
    if (argc < 4){
        printf("usage: ./Whiteboard agent_name network_device port\n");
        int nb = 0;
        char **devices = igs_net_devices_list(&nb);
        printf("Please restart with one of these devices as network_device argument:\n");
        for (int i = 0; i < nb; i++){
            printf(" %s\n", devices[i]);
        }
        igs_free_net_devices_list(devices, nb);
        return 0;
    }

    igs_agent_set_name(argv[1]);
    igs_log_set_console(true);
    igs_log_set_file(true, NULL);
    igs_log_set_stream(true);

    igs_definition_set_class("Whiteboard");

    igs_debug("Ingescape version: %d (protocol v%d)", igs_version(), igs_protocol());

    igs_input_create("title", IGS_STRING_T, 0, 0);
    igs_observe_input("title", myIOCallback, NULL);
    igs_input_create("backgroundColor", IGS_STRING_T, 0, 0);
    igs_observe_input("backgroundColor", myIOCallback, NULL);
    igs_input_create("chatMessage", IGS_STRING_T, 0, 0);
    igs_observe_input("chatMessage", myIOCallback, NULL);
    igs_input_create("clear", IGS_IMPULSION_T, 0, 0);
    igs_observe_input("clear", myIOCallback, NULL);
    igs_input_create("ui_command", IGS_STRING_T, 0, 0);
    igs_observe_input("ui_command", myIOCallback, NULL);
    igs_input_create("labelsVisible", IGS_BOOL_T, 0, 0);
    igs_observe_input("labelsVisible", myIOCallback, NULL);
    igs_output_create("windowWidth", IGS_INTEGER_T, 0, 0);
    igs_output_create("windowHeight", IGS_INTEGER_T, 0, 0);
    igs_output_create("whiteboardWidth", IGS_INTEGER_T, 0, 0);
    igs_output_create("whiteboardHeight", IGS_INTEGER_T, 0, 0);
    igs_output_create("lastChatMessage", IGS_STRING_T, 0, 0);
    igs_output_create("lastAction", IGS_STRING_T, 0, 0);
    igs_output_create("ui_error", IGS_STRING_T, 0, 0);
    igs_service_init("setTitle", myServiceFunction, NULL);
    igs_service_arg_add("setTitle", "title", IGS_STRING_T);
    igs_service_init("setBackgroundColor", myServiceFunction, NULL);
    igs_service_arg_add("setBackgroundColor", "color", IGS_STRING_T);
    igs_service_init("getWindowSize", myServiceFunction, NULL);
    igs_service_reply_add("getWindowSize", "getWindowSizeResult");
    igs_service_reply_arg_add("getWindowSize", "getWindowSizeResult", "width", IGS_INTEGER_T);
    igs_service_reply_arg_add("getWindowSize", "getWindowSizeResult", "height", IGS_INTEGER_T);
    igs_service_init("getWhiteboardSize", myServiceFunction, NULL);
    igs_service_reply_add("getWhiteboardSize", "getWhiteboardSizeResult");
    igs_service_reply_arg_add("getWhiteboardSize", "getWhiteboardSizeResult", "width", IGS_INTEGER_T);
    igs_service_reply_arg_add("getWhiteboardSize", "getWhiteboardSizeResult", "height", IGS_INTEGER_T);
    igs_service_init("chat", myServiceFunction, NULL);
    igs_service_arg_add("chat", "message", IGS_STRING_T);
    igs_service_init("chatAs", myServiceFunction, NULL);
    igs_service_arg_add("chatAs", "name", IGS_STRING_T);
    igs_service_arg_add("chatAs", "message", IGS_STRING_T);
    igs_service_init("snapshot", myServiceFunction, NULL);
    igs_service_reply_add("snapshot", "snapshotResult");
    igs_service_reply_arg_add("snapshot", "snapshotResult", "base64Png", IGS_DATA_T);
    igs_service_init("clear", myServiceFunction, NULL);
    igs_service_init("addShape", myServiceFunction, NULL);
    igs_service_arg_add("addShape", "type", IGS_STRING_T);
    igs_service_arg_add("addShape", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "y", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "width", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "height", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "fill", IGS_STRING_T);
    igs_service_arg_add("addShape", "stroke", IGS_STRING_T);
    igs_service_arg_add("addShape", "strokeWidth", IGS_DOUBLE_T);
    igs_service_reply_add("addShape", "elementCreated");
    igs_service_reply_arg_add("addShape", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("addText", myServiceFunction, NULL);
    igs_service_arg_add("addText", "text", IGS_STRING_T);
    igs_service_arg_add("addText", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addText", "y", IGS_DOUBLE_T);
    igs_service_arg_add("addText", "color", IGS_STRING_T);
    igs_service_reply_add("addText", "elementCreated");
    igs_service_reply_arg_add("addText", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("addImage", myServiceFunction, NULL);
    igs_service_arg_add("addImage", "base64", IGS_DATA_T);
    igs_service_arg_add("addImage", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addImage", "y", IGS_DOUBLE_T);
    igs_service_arg_add("addImage", "width", IGS_DOUBLE_T);
    igs_service_arg_add("addImage", "height", IGS_DOUBLE_T);
    igs_service_reply_add("addImage", "elementCreated");
    igs_service_reply_arg_add("addImage", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("addImageFromUrl", myServiceFunction, NULL);
    igs_service_arg_add("addImageFromUrl", "url", IGS_STRING_T);
    igs_service_arg_add("addImageFromUrl", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addImageFromUrl", "y", IGS_DOUBLE_T);
    igs_service_reply_add("addImageFromUrl", "elementCreated");
    igs_service_reply_arg_add("addImageFromUrl", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("remove", myServiceFunction, NULL);
    igs_service_arg_add("remove", "elementId", IGS_INTEGER_T);
    igs_service_reply_add("remove", "actionResult");
    igs_service_reply_arg_add("remove", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("translate", myServiceFunction, NULL);
    igs_service_arg_add("translate", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("translate", "dx", IGS_DOUBLE_T);
    igs_service_arg_add("translate", "dy", IGS_DOUBLE_T);
    igs_service_reply_add("translate", "actionResult");
    igs_service_reply_arg_add("translate", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("moveTo", myServiceFunction, NULL);
    igs_service_arg_add("moveTo", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("moveTo", "x", IGS_DOUBLE_T);
    igs_service_arg_add("moveTo", "y", IGS_DOUBLE_T);
    igs_service_reply_add("moveTo", "actionResult");
    igs_service_reply_arg_add("moveTo", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("setStringProperty", myServiceFunction, NULL);
    igs_service_arg_add("setStringProperty", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("setStringProperty", "property", IGS_STRING_T);
    igs_service_arg_add("setStringProperty", "value", IGS_STRING_T);
    igs_service_reply_add("setStringProperty", "actionResult");
    igs_service_reply_arg_add("setStringProperty", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("setDoubleProperty", myServiceFunction, NULL);
    igs_service_arg_add("setDoubleProperty", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("setDoubleProperty", "property", IGS_STRING_T);
    igs_service_arg_add("setDoubleProperty", "value", IGS_DOUBLE_T);
    igs_service_reply_add("setDoubleProperty", "actionResult");
    igs_service_reply_arg_add("setDoubleProperty", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("getElementIds", myServiceFunction, NULL);
    igs_service_reply_add("getElementIds", "elementIds");
    igs_service_reply_arg_add("getElementIds", "elementIds", "jsonArray", IGS_STRING_T);
    igs_service_init("getElements", myServiceFunction, NULL);
    igs_service_reply_add("getElements", "elements");
    igs_service_reply_arg_add("getElements", "elements", "jsonArray", IGS_STRING_T);
    igs_service_init("showLabels", myServiceFunction, NULL);
    igs_service_init("hideLabels", myServiceFunction, NULL);

    igs_start_with_device(argv[2], atoi(argv[3]));

    getchar();

    igs_stop();
    return 0;
}

