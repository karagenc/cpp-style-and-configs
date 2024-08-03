#include "proto_z.h"

#include <iostream>
#include <mutex>
#include <set>

// proto-z is an imaginary interstellar communication protocol.
namespace proto_z
{
    // Static variables are prefixed with s_
    int InterstellarLink::s_send_count = 0;

    // Global variables are prefixed with g_
    std::set<Addr> g_sent_addrs;
    std::mutex g_mu;

    void Server::send_message(const Addr &to, const std::string &message)
    {
        Header header = {
            m_addr,
            to,
            message,
        };

        std::lock_guard<std::mutex> guard(g_mu);
        g_sent_addrs.insert(to);
        s_send_count++;
        std::cout << "Number of total packets sent: " << s_send_count << "\n";

        // ...
    }

    void Server::recv_message(const Addr &to, const std::string &message)
    {
        // ...
    }

    void Client::send_message(const Addr &to, const std::string &message)
    {
        Header header = {
            m_addr,
            to,
            message,
        };

        std::lock_guard<std::mutex> guard(g_mu);
        g_sent_addrs.insert(to);
        s_send_count++;
        std::cout << "Number of total packets sent: " << s_send_count << "\n";

        // ...
    }

    void recv_message(const Addr &to, const std::string &message)
    {
        // ...
    }
}
